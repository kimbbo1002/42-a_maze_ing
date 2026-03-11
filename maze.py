import random
import os
from typing import Dict, Any, List
from Enums import ConfigOptions, Colors
from cell import Cell


class Maze:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.cols = config[ConfigOptions.WIDTH]
        self.rows = config[ConfigOptions.HEIGHT]
        self.grid_cells = [Cell(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.seed = random.choice(range(1000))
        self.display = ""
    
    def set_seed(self, seed: int) -> None:
        print(f"\n[Setting Seed ...]")
        self.seed = seed
        print(
            f"{Colors.GREEN}SUCCESS: "
            f"{Colors.RESET}Seed setted to {seed}."
        )
    
    def remove_walls(self, current: Cell, next: Cell) -> None:
        dx = current.x - next.x
        if dx == 1:
            current.knock_down_wall(next, 'W')
        elif dx == -1:
            current.knock_down_wall(next, 'E')

        dy = current.y - next.y
        if dy == 1:
            current.knock_down_wall(next, 'N')
        elif dy == -1:
            current.knock_down_wall(next, 'S')
    
    def generate_maze(self) -> None:
        print("\n[Generating Maze ...]")
        if self.config[ConfigOptions.FORTYTWO]:
            self.add_42_pattern()
        entry_x, entry_y = self.config[ConfigOptions.ENTRY]
        current_cell = Cell.check_cell(entry_x, entry_y, self.cols, self.rows, self.grid_cells)
        stack = []
        cell_count = 1
        target = len([c for c in self.grid_cells if not c.fortytwo])
        random.seed(self.seed)
        while cell_count < target:
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(self.cols, self.rows, self.grid_cells)
            if next_cell:
                next_cell.visited = True
                cell_count += 1
                stack.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()
    
    def check_cell(self, x: int, y:int) -> Cell:
        find_index = lambda x, y: x + y * self.cols
        return self.grid_cells[find_index(x, y)]

    def add_42_pattern(self) -> None:
        
        mid_x = self.cols // 2
        mid_y = self.rows // 2
        
        pattern_coordinates = [
            (mid_x - 3, mid_y - 2),
            (mid_x - 3, mid_y - 1),
            (mid_x - 3, mid_y),
            (mid_x - 2, mid_y),
            (mid_x - 1, mid_y),
            (mid_x - 1, mid_y + 1),
            (mid_x - 1, mid_y + 2),
            (mid_x + 1, mid_y - 2),
            (mid_x + 2, mid_y - 2),
            (mid_x + 3, mid_y - 2),
            (mid_x + 3, mid_y - 1),
            (mid_x + 3, mid_y),
            (mid_x + 2, mid_y),
            (mid_x + 1, mid_y),
            (mid_x + 1, mid_y + 1),
            (mid_x + 1, mid_y + 2),
            (mid_x + 2, mid_y + 2),
            (mid_x + 3, mid_y + 2)
        ]

        for x, y in pattern_coordinates:
            Cell.check_cell(x, y, self.cols, self.rows, self.grid_cells).fortytwo = True
        
        entry_exit = [
            self.config[ConfigOptions.ENTRY],
            self.config[ConfigOptions.EXIT]
        ]
        for x, y in entry_exit:
            if Cell.check_cell(x, y, self.cols, self.rows, self.grid_cells).fortytwo:
                raise ValueError(
                    f"{Colors.RED}ERROR: "
                    f"{Colors.RESET}Entry or Exit cannot be on the 42 pattern.\n"
                )

    def display_maze(self) -> None:
        print("\n[Displaying Maze ...]")
        count = 0
        try:
            os.remove(self.config[ConfigOptions.OUTPUT_FILE])
        except OSError:
            pass
        for cell in self.grid_cells:
            self.display += cell.display()
            count += 1
            if count % self.cols == 0:
                self.display += '\n'
        with open(self.config[ConfigOptions.OUTPUT_FILE], 'w') as file:
            file.write(self.display)