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

    def display(self, file_name: str) -> None:
        bit = 0
        if self.walls['N']:
            bit |= 1
        if self.walls['E']:
            bit |= 1 << 1
        if self.walls['S']:
            bit |= 1 << 2
        if self.walls['W']:
            bit |= 1 << 3
        
        with open(file_name, 'a') as file:
            file.write(format(bit, 'X'))

    def check_cell(self, x: int, y: int, cols: int, rows: int, grid_cells: list) -> Cell:
        find_index = lambda x, y: x + y * cols # 2D grid into a 1D list
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self, cols: int, rows: int, grid_cells: list) -> Cell | bool:
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
        if top and not top.visited and not top.fortytwo: 
            neighbors.append(top)
        if bottom and not bottom.visited and not bottom.fortytwo:
            neighbors.append(bottom)
        if right and not right.visited and not right.fortytwo:
            neighbors.append(right)
        if left and not left.visited and not left.fortytwo:
            neighbors.append(left)
        
        return random.choice(neighbors) if neighbors else False
    
    def knock_down_wall(self, other: Cell, wall: str) -> None:
        """Knock down the wall between cells self and other."""
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

