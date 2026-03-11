from typing import Dict, Any
from Enums import Colors, ConfigOptions
from parsing_config import check_config
from maze import Maze



def main() -> None:
    config: Dict[ConfigOptions, Any]

    try:
        # phase1: reading from config file
        config = check_config()
        # print(config)

        # phase2: generating random maze
        maze = Maze(config)
        maze.generate_maze()
        maze.display_maze()
        
    except Exception as e:
        print(e)
        return
    
    


main()
