import sys
from typing import Dict, Any, List
from Enums import Colors, ConfigOptions


def check_config() -> Dict[ConfigOptions, Any]:
    file_name: str
    width: int
    height: int
    entry: List[int] = []
    exit: List[int] = []
    output: str
    perfect: bool
    fortytwo: bool

    print("\n[Analyzing Configurations ...]")
    if not len(sys.argv) == 2:
        raise ValueError(
            f"{Colors.RED}ERROR: "
            f"{Colors.RESET}Wrong number of arguments were input.\n"
            "(command example) python3 a_maze_ing.py config.txt"
        )
    file_name = sys.argv[1]

    # check file existence
    try:
        with open(file_name, 'r') as file:
            for line in file:
                key, value = line.split('=')
                # check config formatting
                try:
                    if key == ConfigOptions.WIDTH.value:
                        width = int(value)
                    elif key == ConfigOptions.HEIGHT.value:
                        height = int(value)
                    elif key == ConfigOptions.ENTRY.value:
                        tmp1, tmp2 = value.split(',')
                        entry.extend([int(tmp1), int(tmp2)])
                    elif key == ConfigOptions.EXIT.value:
                        tmp1, tmp2 = value.split(',')
                        exit.extend([int(tmp1), int(tmp2)])
                    elif key == ConfigOptions.OUTPUT_FILE.value:
                        tmp = value.split('.')
                        if not tmp[1].strip() == "txt":
                            raise ValueError
                        output = value
                    elif key == ConfigOptions.PERFECT.value:
                        if value == "True":
                            perfect = True
                        elif value == "False":
                            perfect = False
                        else:
                            raise ValueError
                    else:
                        continue

                except Exception:
                    raise ValueError(
                        f"{Colors.RED}ERROR: "
                        f"{Colors.RESET}Wrong configuration formatting.\n"
                        "Mandatory keys with example values:\n"
                        "WIDTH=20\nHEIGHT=15\nENTRY=0,0\n"
                        "EXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True"
                    )

        try:
            _ = (width, height, entry, exit, output, perfect):
        except UnboundLocalError:
            raise ValueError(
                f"{Colors.RED}ERROR: "
                f"{Colors.RESET}Mandatory key missing.\n"
                "Mandatory keys with example values:\n"
                "WIDTH=20\nHEIGHT=15\nENTRY=0,0\n"
                "EXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True"
            )

    except FileNotFoundError:
        raise FileNotFoundError(
            f"{Colors.RED}ERROR: "
            f"{Colors.RESET}File ({file_name}) could not be found.\n"
            "Make sure the file exists."
        )

    # check impossible maze parameters
    if (
        width <= 0 or height <= 0
        or not (0 <= entry[0] < width and 0 <= entry[1] < height)
        or not (0 <= exit[0] < width and 0 <= exit[1] < height)
        or entry == exit
    ):
        raise ValueError(
            f"{Colors.RED}ERROR: "
            f"{Colors.RESET}Impossible maze parameter detected.\n"
            "Check if ...\n"
            "1) Width and Height are not equal or below 0\n"
            "2) Entry and Exit coordinates belong in the maze\n"
            "3) Entry and Exit are not the same coordinates"
        )
    
    # check if 42 pattern fits
    if width < 9 or height < 7:
        fortytwo = False
        print(
            f"{Colors.YELLOW}WARNING: "
            f"{Colors.RESET}Size is too small to insert the '42' pattern."
        )
    else:
        fortytwo = True

    print(
        f"{Colors.GREEN}SUCCESS: "
        f"{Colors.RESET}Configuration file successfully analyzed."
    )
    return {
        ConfigOptions.WIDTH: width,
        ConfigOptions.HEIGHT: height,
        ConfigOptions.ENTRY: entry,
        ConfigOptions.EXIT: exit,
        ConfigOptions.OUTPUT_FILE: output.strip(),
        ConfigOptions.PERFECT: perfect,
        ConfigOptions.FORTYTWO: fortytwo
    }
