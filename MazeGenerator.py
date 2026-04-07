from maze import Maze
from config import check_config
from typing import Optional
import random

class MazeGenerator:
    def __init__(self, seed: Optional[int]) -> None:
        self.seed = seed if seed else random.choice(range(1000))
    
    def generate_maze(self) -> Optional[Maze]:
        try:
            config = check_config()
            maze = Maze(config)
            maze.set_seed(self.seed)
            maze.generate_maze()
            maze.get_path()
            maze.display_output_file()
            return maze
        except Exception as e:
            print(e)