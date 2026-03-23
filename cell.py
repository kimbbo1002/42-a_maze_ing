from __future__ import annotations
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

    def display(self) -> str:
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
    def check_cell(x: int, y: int, cols: int, rows: int, grid_cells: list) -> Cell | bool:
        find_index = lambda x, y: x + y * cols # 2D grid into a 1D list
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def is_large_open_area(self, cols: int, rows: int, grid_cells: list) -> bool:
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < cols and 0 <= ny < rows:
                    if not Cell.check_cell(nx, ny, cols, rows, grid_cells).visited:
                        continue
                    count += 1
        return count >= 9

    def check_neighbors(self, cols: int, rows: int, grid_cells: list) -> Cell | bool:
        neighbors = []
        top = Cell.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        bottom = Cell.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        right = Cell.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        left = Cell.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
        for n in [top, bottom, right, left]:
            if n and not n.visited and not n.fortytwo:
                if n.is_large_open_area(n.x, n.y, cols, rows, grid_cells):
                    continue
                neighbors.append(n)
        
        return random.choice(neighbors) if neighbors else False
    
    def knock_down_wall(self, other: Cell, wall: str) -> None:
        """Knock down the wall between cells self and other."""
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

