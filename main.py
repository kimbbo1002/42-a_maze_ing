from typing import Dict, Any
from enums import Colors, ConfigOptions
from config import check_config
from maze import Maze


def main() -> None:
    config: Dict[ConfigOptions, Any]

    try:
        # phase1: reading from config file
        config = check_config()
        
        
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    main()
