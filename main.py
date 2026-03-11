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
        maze.set_seed(42)
        maze.generate_maze()
        print(
            f"{Colors.GREEN}SUCCESS: "
            f"{Colors.RESET}Maze generated."
        )
        maze.display_maze()
        print(
            f"{Colors.GREEN}SUCCESS: "
            f"{Colors.RESET}Maze displayed to {config[ConfigOptions.OUTPUT_FILE].strip()}."
        )
        
    except Exception as e:
        print(e)
        return
    
    


main()
