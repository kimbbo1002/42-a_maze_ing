#!/usr/bin/env python3
from mazegen import MazeGenerator
from mazegen import display_maze


def main() -> None:
    try:
        generator = MazeGenerator(None)
        maze = generator.generate_maze()
        display_maze(maze)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
