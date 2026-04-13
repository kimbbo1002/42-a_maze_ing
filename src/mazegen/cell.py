from __future__ import annotations
from typing import List
import random


class Cell:

    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the cell at (x,y). At first it is surrounded by walls.
        """
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False
        self.fortytwo = False
        self.path = False
        self.entry = False
        self.exit = False

    def display_in_hex(self) -> str:
        bit = 0
        if self.walls['N']:
            bit |= 1
        if self.walls['E']:
            bit |= 1 << 1
        if self.walls['S']:
            bit |= 1 << 2
        if self.walls['W']:
            bit |= 1 << 3

        return (format(bit, 'X'))

    @staticmethod
    def check_cell(
        x: int, y: int, cols: int, rows: int, grid_cells: List[Cell]
    ) -> Cell | None:
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return None
        return grid_cells[x + y * cols]  # 2D grid into a 1D list

    def check_neighbors(
            self, cols: int, rows: int, grid_cells: List[Cell]
    ) -> Cell | None:
        neighbors = []
        top = Cell.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        bottom = Cell.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        right = Cell.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        left = Cell.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
        for n in [top, bottom, right, left]:
            if n and not n.visited and not n.fortytwo:
                neighbors.append(n)

        return random.choice(neighbors) if neighbors else None

    def knock_down_wall(self, other: Cell, wall: str) -> None:
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False
