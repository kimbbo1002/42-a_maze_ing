#!/usr/bin/env python3
from src import MazeGenerator, display_maze, Colors


def main() -> None:
    try:
        generator = MazeGenerator(seed=42)
        maze = generator.generate_maze()
        if maze is None:
            raise ValueError(
                f"{Colors.DIM}ERROR: Maze generation failed")
        display_maze(maze)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
