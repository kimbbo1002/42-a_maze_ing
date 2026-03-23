import random
import os
from typing import Dict, Any, List
from enums import ConfigOptions, Colors
from cell import Cell


class Maze:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.cols = config[ConfigOptions.WIDTH]
        self.rows = config[ConfigOptions.HEIGHT]
        self.grid_cells = [Cell(col, row) for row in range(self.rows) for col in range(self.cols)]
    
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
        if self.config[ConfigOptions.FORTYTWO]:
            self.add_42_pattern()
        current_cell = self.grid_cells[0]
        array = []
        cell_count = 1
        while cell_count != len(self.grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(self.cols, self.rows, self.grid_cells)
            if next_cell:
                next_cell.visited = True
                cell_count += 1
                array.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
    
    def check_cell(self, x: int, y:int) -> Cell:
        find_index = lambda x, y: x + y * self.cols # 2D grid into a 1D list
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def add_42_pattern(self) -> None:
        
        mid_x = self.cols // 2
        mid_y = self.rows // 2

        self.check_cell(mid_x - 3, mid_y - 2).fortytwo = True
        self.check_cell(mid_x - 3, mid_y - 1).fortytwo = True
        self.check_cell(mid_x - 3, mid_y).fortytwo = True
        self.check_cell(mid_x - 2, mid_y).fortytwo = True
        self.check_cell(mid_x - 1, mid_y).fortytwo = True
        self.check_cell(mid_x - 1, mid_y + 1).fortytwo = True
        self.check_cell(mid_x - 1, mid_y + 2).fortytwo = True

        self.check_cell(mid_x + 1, mid_y + 2).fortytwo = True
        self.check_cell(mid_x + 2, mid_y + 2).fortytwo = True
        self.check_cell(mid_x + 3, mid_y + 2).fortytwo = True
        self.check_cell(mid_x + 3, mid_y + 1).fortytwo = True
        self.check_cell(mid_x + 3, mid_y).fortytwo = True
        self.check_cell(mid_x + 2, mid_y).fortytwo = True
        self.check_cell(mid_x + 1, mid_y).fortytwo = True
        self.check_cell(mid_x + 1, mid_y - 1).fortytwo = True
        self.check_cell(mid_x + 1, mid_y - 2).fortytwo = True
        self.check_cell(mid_x + 2, mid_y - 2).fortytwo = True
        self.check_cell(mid_x + 3, mid_y - 2).fortytwo = True

    def display_maze(self) -> None:
        count = 0
        try:
            os.remove(self.config[ConfigOptions.OUTPUT_FILE])
        except OSError:
            pass
        for cell in self.grid_cells:
            cell.display(self.config[ConfigOptions.OUTPUT_FILE])
            count += 1
            if count % self.cols == 0:
                file = open(self.config[ConfigOptions.OUTPUT_FILE], 'a')
                file.write('\n')
                file.close()