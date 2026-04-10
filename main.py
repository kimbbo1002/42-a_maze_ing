#!/usr/bin/env python3
from MazeGenerator import MazeGenerator
from display_maze import display_maze


def main() -> None:
    generator = MazeGenerator(None)
    maze = generator.generate_maze()
    display_maze(maze)


if __name__ == "__main__":
    main()
