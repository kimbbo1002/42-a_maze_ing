import random
import sys
import tty
import termios
from ..mazegen import Maze
from .maze_themes import COLOR_SETTINGS

RESET = "\033[0m"
CLEAR = "\033[2J\033[H"
CELL_W = "  "  # width cell (in spaces)
CELL_H = 1  # height cell (in lines)


def read_key() -> str:
    fd = sys.stdin.fileno()  # return 0 for input (keyboard)
    old_settings = termios.tcgetattr(fd)  # save current keyboard config
    try:
        tty.setraw(fd)  # change keyboard input method to -> read instantly
        return sys.stdin.read(1)
    finally:
        # reset keyboard config to -> normal state (old settings)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_cell_color(cell, colors: dict, show_path: bool) -> str:
    if cell.entry:
        return colors["entry"]
    if cell.exit:
        return colors["exit"]
    if cell.fortytwo:
        return colors["fortytwo"]
    if cell.path and show_path:
        return colors["path"]
    return colors["cell"]


def get_maze_output(maze, colors: dict, show_path: bool) -> str:
    output = CLEAR
    wall_color = colors["wall"]

    # 1. Bordure supérieure (Mur Nord global)
    top_border = wall_color + (CELL_W * (2 * maze.cols + 1)) + RESET + "\n"
    output += top_border * CELL_H

    for row in range(maze.rows):
        line_up = wall_color + CELL_W + RESET
        line_low = wall_color + CELL_W + RESET

        for col in range(maze.cols):
            cell = maze.grid_cells[row * maze.cols + col]
            color = get_cell_color(cell, colors, show_path)

            # Cell + East Wall
            line_up += color + CELL_W + RESET
            if cell.walls['E']:
                line_up += wall_color + CELL_W + RESET
            else:
                next_cell = maze.grid_cells[row * maze.cols + col + 1]
                # path color only if current.path and next.path (avoid outflow)
                if show_path and cell.path and next_cell.path:
                    line_up += colors['path'] + CELL_W + RESET
                else:
                    line_up += colors['cell'] + CELL_W + RESET

            # South Wall + Corner
            if cell.walls['S']:
                line_low += wall_color + CELL_W + RESET
            else:
                next_cell = maze.grid_cells[(row + 1) * maze.cols + col]
                if show_path and cell.path and next_cell.path:
                    line_low += colors['path'] + CELL_W + RESET
                else:
                    line_low += colors['cell'] + CELL_W + RESET
            # corner (always a wall btw 4 cells)
            line_low += wall_color + CELL_W + RESET

        # repeat each line * CELL_H time
        for _ in range(CELL_H):
            output += line_up + "\n"
        for _ in range(CELL_H):
            output += line_low + "\n"

    return output


def render_controls(color_name: str, show_path: bool) -> str:
    path_status = "ON ✓" if show_path else "OFF"
    return (
        f"\n  ==== A-MAZE-ING render control ====\n"
        f"\n  Theme : {color_name}\n"
        f"  [C] Change Maze colors\n"
        f"  [P] Path : {path_status}\n"
        f"  [R] Re-generate a new Maze\n"
        f"  [Q] Quit\n"
        f"  Your choice : "
    )


def display_maze(maze) -> None:
    color_index = random.randint(0, len(COLOR_SETTINGS) - 1)

    while True:
        colors = COLOR_SETTINGS[color_index]

        output = get_maze_output(maze, colors, maze.show_path)
        output += render_controls(colors["name"], maze.show_path)
        sys.stdout.write(output)
        sys.stdout.flush()

        key = read_key().lower()

        if key == 'q':
            sys.stdout.write(CLEAR)
            break

        elif key == 'c':
            color_index = (color_index + 1) % len(COLOR_SETTINGS)

        elif key == 'p':
            maze.show_path = not maze.show_path

        elif key == 'r':
            CLEAR
            show_path = maze.show_path
            maze = Maze(maze.config)
            maze.generate_maze()
            maze.get_path()
            maze.show_path = show_path
            maze.display_output_file()
