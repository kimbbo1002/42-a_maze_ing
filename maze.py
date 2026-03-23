import random
import os
from typing import Dict, Any, List
from Enums import ConfigOptions, Colors
from cell import Cell


class Maze:
    def __init__(self, config: dict, themes: dict) -> None:
        self.config = config
        self.cols = config[ConfigOptions.WIDTH]
        self.rows = config[ConfigOptions.HEIGHT]
        self.grid_cells = [Cell(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.seed = random.choice(range(1000))
        self.display = ""
        self.path = []
        self.show_path = False
        self.themes = themes
        self.theme_name = list(themes.keys()[0])
        self.colors = dict(themes[self.theme_name])
    
    def reset(self) -> None:
        self.grid_cells = [Cell(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.seed = random.choice(range(1000))
        self.display = ""
        self.path = []
        self.show_path = False
    
    def set_seed(self, seed: int) -> None:
        self.seed = seed
    
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
        target = sum(1 for c in self.grid_cells if not c.fortytwo)

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


    def add_42_pattern(self) -> None:
        mid_x = self.cols // 2
        mid_y = self.rows // 2
        
        pattern_coordinates = [
            (-3,-2),(-3,-1),(-3, 0),(-2, 0),(-1, 0),(-1, 1),(-1, 2),
            ( 1,-2),( 2,-2),( 3,-2),( 3,-1),( 3, 0),( 2, 0),( 1, 0),
            ( 1, 1),( 1, 2),( 2, 2),( 3, 2)
        ]

        for dx, dy in pattern_coordinates:
            Cell.check_cell(mid_x + dx, mid_y + dy, self.cols, self.rows, self.grid_cells).fortytwo = True
        
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


    def get_path(self, draw_fn: callable) -> None:
        entry_x, entry_y = self.config[ConfigOptions.ENTRY]
        exit_x, exit_y = self.config[ConfigOptions.EXIT]
        entry = Cell.check_cell(entry_x, entry_y, self.cols, self.rows, self.grid_cells)
        exit = Cell.check_cell(exit_x, exit_y, self.cols, self.rows, self.grid_cells)

        direction = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
        stack = [entry]
        visited = {entry: None}

        while stack:
            current = stack.pop()
            if current is exit:
                break
            for wall, (dx, dy) in direction.items():
                if not current.walls[wall]:
                    next = Cell.check_cell(current.x + dx, current.y + dy, self.cols, self.rows, self.grid_cells)
                    if next and next not in visited:
                        visited[next] = current
                        stack.append(next)
        
        path_cell = exit
        while path_cell is not None:
            self.path.append(path_cell)
            path_cell = visited.get(path_cell)
        self.path.reverse()

        draw_fn(self.grid_cells, self.cols, self.colors, self.path)


    def get_path_output(self) -> None:
        entry_x, entry_y = self.config[ConfigOptions.ENTRY]
        exit_x, exit_y = self.config[ConfigOptions.EXIT]
        entry = Cell.check_cell(entry_x, entry_y, self.cols, self.rows, self.grid_cells)
        exit = Cell.check_cell(exit_x, exit_y, self.cols, self.rows, self.grid_cells)

        direction = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
        stack = [entry]
        visited = {entry: None}

        while stack:
            current = stack.pop()
            if current is exit:
                break
            for wall, (dx, dy) in direction.items():
                if not current.walls[wall]:
                    next = Cell.check_cell(current.x + dx, current.y + dy, self.cols, self.rows, self.grid_cells)
                    if next and next not in visited:
                        visited[next] = current
                        stack.append(next)
        
        path = []
        path_cell = exit
        while visited[path_cell][0] is not None:
            before, now = visited[path_cell]
            path.append(now)
            path_cell = before
        
        path.reverse
        return path


    def toggle_path(self, draw_fn: callable) -> None:
        self.show_path = not self.show_path
        if self.show_path and not self.path:
            self.get_path(draw_fn)
        else:
            draw_fn(self.grid_cells, self.cols, self.colors, self.path if self.show_path else None)


    def display_output_file(self) -> None:
        print("\n[Displaying Maze ...]")
        count = 0
        for cell in self.grid_cells:
            self.display += cell.display()
            count += 1
            if count % self.cols == 0:
                self.display += '\n'

        entry_x, entry_y = self.config[ConfigOptions.ENTRY]
        exit_x,  exit_y  = self.config[ConfigOptions.EXIT]
        self.display += f"\n\n{entry_x},{entry_y}\n"
        self.display += f"{exit_x},{exit_y}\n"
        self.display += "".join(self.get_path_output()) + "\n"

        try:
            os.remove(self.config[ConfigOptions.OUTPUT_FILE])
        except OSError:
            pass
        with open(self.config[ConfigOptions.OUTPUT_FILE], 'w') as file:
            file.write(self.display)
        
