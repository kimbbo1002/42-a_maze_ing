import sys
import tty
import termios
from Enums import ConfigOptions
from cell import Cell
from maze import Maze


RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"


def bg(r, g, b): 
    return f"\033[48;2;{r};{g};{b}m"


def fg(r, g, b): 
    return f"\033[38;2;{r};{g};{b}m"


def clear():     sys.stdout.write("\033[H\033[2J"); sys.stdout.flush()


def get_key() -> str:
    fd = sys.stdin.fileno()
    save = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return f"\x1b{ch2}{ch3}"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, save)


KEY_UP = '\x1b[A'
KEY_DOWN = '\x1b[B'
KEY_RIGHT = '\x1b[C'
KEY_LEFT = '\x1b[D'
KEY_ENTER = '\r'
KEY_ESC = '\x1b'


THEMES = {
    "Classic": {
        "wall":      ( 40,  40,  40),
        "visited":   (200, 200, 200),
        "unvisited": ( 20,  20,  20),
        "path":      (255, 220,  50),
        "fortytwo":  (255,  60,  60),
        "current":   ( 50, 220,  50),
        "stack":     ( 50, 100, 220),
    },
    "Ocean": {
        "wall":      (  0,  40,  80),
        "visited":   ( 80, 160, 200),
        "unvisited": (  0,  20,  50),
        "path":      (  0, 255, 200),
        "fortytwo":  (255, 140,   0),
        "current":   (  0, 220, 255),
        "stack":     (  0,  80, 160),
    },
    "Lava": {
        "wall":      ( 40,   0,   0),
        "visited":   (180,  60,   0),
        "unvisited": ( 20,   0,   0),
        "path":      (255, 220,  50),
        "fortytwo":  (255, 255, 255),
        "current":   (255, 100,   0),
        "stack":     (140,  20,   0),
    },
    "Forest": {
        "wall":      ( 20,  40,  10),
        "visited":   ( 80, 140,  50),
        "unvisited": ( 10,  20,   5),
        "path":      (220, 255, 100),
        "fortytwo":  (255, 180,   0),
        "current":   (150, 255,  50),
        "stack":     ( 40,  80,  20),
    },
    "Neon": {
        "wall":      ( 10,  10,  30),
        "visited":   ( 40,  40,  80),
        "unvisited": (  5,   5,  20),
        "path":      (255,   0, 255),
        "fortytwo":  (  0, 255, 255),
        "current":   (255,   0, 128),
        "stack":     ( 80,   0, 200),
    }
}

THEME_NAMES = list(THEMES.keys())


def draw_maze(grid_cells: list, cols: int, rows: int, colors: dict, current: Cell, stack: list, path: list, entry: tuple, exit: tuple):
    path_set = set(path) if path else set()

    entry_x, entry_y = entry
    exit_x, exit_y = exit