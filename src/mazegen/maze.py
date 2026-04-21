import random
import os
from .enums import ConfigOptions, Colors
from .cell import Cell
from typing import List, Dict, Any


class Maze:
    def __init__(self, config: dict[ConfigOptions, Any]) -> None:
        self.config = config
        self.cols = config[ConfigOptions.WIDTH]
        self.rows = config[ConfigOptions.HEIGHT]
        self.grid_cells = [Cell(col, row) for row in range(self.rows)
                           for col in range(self.cols)]
        self.seed = random.choice(range(1000))
        self.display = ""
        self.path: List[str] = []
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
        current_cell = Cell.check_cell(entry_x, entry_y, self.cols,
                                       self.rows, self.grid_cells)
        if current_cell:
            current_cell.entry = True

        exit_x, exit_y = self.config[ConfigOptions.EXIT]
        exit_cell = Cell.check_cell(exit_x, exit_y, self.cols,
                                    self.rows, self.grid_cells)
        if exit_cell:
            exit_cell.exit = True

        stack = []
        cell_count = 1
        target = sum(1 for c in self.grid_cells if not c.fortytwo)

        random.seed(self.seed)
        while cell_count < target:
            if current_cell:
                current_cell.visited = True
                next_cell = current_cell.check_neighbors(self.cols, self.rows,
                                                         self.grid_cells)
                if next_cell:
                    next_cell.visited = True
                    cell_count += 1
                    stack.append(current_cell)
                    self.remove_walls(current_cell, next_cell)
                    current_cell = next_cell
                elif stack:
                    current_cell = stack.pop()
        print(
            f"{Colors.GREEN}GENERATION SUCCESS: {Colors.RESET}"
            "Maze was successfully generated."
        )

    def add_42_pattern(self) -> None:
        mid_x = self.cols // 2
        mid_y = self.rows // 2

        pattern_coordinates = [
            (-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, 0), (-1, 1), (-1, 2),
            (1, -2), (2, -2), (3, -2), (3, -1), (3, 0), (2, 0), (1, 0),
            (1, 1), (1, 2), (2, 2), (3, 2)
        ]

        for dx, dy in pattern_coordinates:
            pattern_cell = Cell.check_cell(mid_x + dx, mid_y + dy, self.cols,
                                           self.rows, self.grid_cells)
            if pattern_cell:
                pattern_cell.fortytwo = True

        entry_exit = [
            self.config[ConfigOptions.ENTRY],
            self.config[ConfigOptions.EXIT]
        ]
        for x, y in entry_exit:
            e_cell = Cell.check_cell(x, y, self.cols, self.rows,
                                     self.grid_cells)
            if e_cell and e_cell.fortytwo:
                raise ValueError(
                    f"{Colors.RED}ERROR: "
                    f"{Colors.RESET}Entry or Exit cannot be "
                    "on the 42 pattern.\n"
                )

    def get_path(self) -> None:
        entry_x, entry_y = self.config[ConfigOptions.ENTRY]
        exit_x, exit_y = self.config[ConfigOptions.EXIT]
        entry = Cell.check_cell(entry_x, entry_y, self.cols,
                                self.rows, self.grid_cells)
        exit = Cell.check_cell(exit_x, exit_y, self.cols,
                               self.rows, self.grid_cells)

        direction = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        stack = [entry]
        visited: Dict[Cell | None, Cell | None] = {entry: None}

        while stack:
            current = stack.pop()
            if current == exit:
                break
            for wall, (dx, dy) in direction.items():
                if current and not current.walls[wall]:
                    next = Cell.check_cell(
                        current.x + dx, current.y + dy,
                        self.cols, self.rows, self.grid_cells)
                    if next and next not in visited:
                        visited[next] = current
                        stack.append(next)

        path_cell = exit
        tmp_path = []
        while path_cell is not None:
            tmp_path.append(path_cell)
            path_cell.path = True
            path_cell = visited.get(path_cell)
        tmp_path.reverse()

        for i in range(len(tmp_path) - 1):
            current = tmp_path[i]
            next = tmp_path[i + 1]

            dx = next.x - current.x
            dy = next.y - current.y

            if dx == 1:
                self.path.append('E')
            elif dx == -1:
                self.path.append('W')
            elif dy == 1:
                self.path.append('S')
            elif dy == -1:
                self.path.append('N')

    def display_output_file(self) -> None:
        print("\n[Writing to OUTPUT_FILE ...]")
        count = 0
        for cell in self.grid_cells:
            self.display += cell.display_in_hex()
            count += 1
            if count % self.cols == 0:
                self.display += '\n'

        entry_x, entry_y = self.config[ConfigOptions.ENTRY]
        exit_x, exit_y = self.config[ConfigOptions.EXIT]
        self.display += f"\n{entry_x},{entry_y}\n"
        self.display += f"{exit_x},{exit_y}\n"
        self.display += "".join(self.path) + "\n"

        try:
            os.remove(self.config[ConfigOptions.OUTPUT_FILE])
        except OSError:
            pass
        with open(self.config[ConfigOptions.OUTPUT_FILE], 'w') as file:
            file.write(self.display)

        print(
            f"{Colors.GREEN}OUTPUT SUCCESS: {Colors.RESET}"
            "OUTPUT_FILE was successfully generated"
        )
