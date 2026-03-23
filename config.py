import sys
from typing import List
from pydantic import BaseModel, field_validator, model_validator
from Enums import Colors, ConfigOptions


class Config(BaseModel):
    width: int
    height: int
    entry: List[int]
    exit: List[int]
    output_file: str
    perfect: bool
    fortytwo: bool = False

    @field_validator("output_file")
    @classmethod
    def check_output_file(cls, value: str) -> str:
        if not value.strip().endswith(".txt"):
            raise ValueError("OUTPUT_FILE must have a .txt extension")
        return value.strip()
    
    @field_validator("entry", "exit")
    @classmethod
    def check_entry_exit(cls, value: List[int]) -> List[int]:
        if len(value) != 2:
            raise ValueError("ENTRY / EXIT must be two comma-separated integers")
        return value
    
    @model_validator(mode="after")
    def check_maze_logic(self) -> "Config":
        w, h = self.width, self.height
        if w <= 0 or h <= 0:
            raise ValueError("Width and Height must be greater than 0")
        if not (0 <= self.entry[0] < w and 0 <= self.entry[1] < h):
            raise ValueError("Entry coordinates are out of maze bound")
        if not (0 <= self.exit[0] < w and 0 <= self.exit[1] < h):
            raise ValueError("Exit coordinates are out of maze bound")
        if self.entry == self.exit:
            raise ValueError("Entry and Exit cannot be the same coordinates")
        
        self.fortytwo = w >= 9 and h >= 7
        if not self.fortytwo:
            print(
                f"{Colors.YELLOW}WARNING: {Colors.RESET}"
                "Size is too small to insert the '42' pattern."
            )

        return self


def parse_raw_config(file_name: str) -> dict:
    raw = {}
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, _, value = line.partition("=")
            raw[key.strip()] = value.strip()
    
    return {
        "width": int(raw[ConfigOptions.WIDTH.value]),
        "height": int(raw[ConfigOptions.HEIGHT.value]),
        "entry": [int(x) for x in raw[ConfigOptions.ENTRY.value].split(",")],
        "exit": [int(x) for x in raw[ConfigOptions.EXIT.value].split(",")],
        "output_file": raw[ConfigOptions.OUTPUT_FILE.value],
        "perfect": raw[ConfigOptions.PERFECT.value] == "True",
    }


def check_config() -> dict:
    print("\n[Analyzing Configurations ...]")

    if len(sys.argv) != 2:
        raise ValueError(
            f"{Colors.RED}ERROR: {Colors.RESET}"
            "Wrong number of arguments.\n"
            "(example) python3 a_maze_ing.py config.txt"
        )
    
    file_name = sys.argv[1]
    try:
        raw = parse_raw_config(file_name)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"{Colors.RED}ERROR: {Colors.RESET}"
            f"File ({file_name}) could not be found."
        )
    except (KeyError, ValueError):
        raise ValueError(
            f"{Colors.RED}ERROR: {Colors.RESET}"
            "Wrong configuration formatting.\n"
            "Mandatory keys with example values:\n"
            "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
            "OUTPUT_FILE=maze.txt\nPERFECT=True"
        )
    
    try:
        config = Config(**raw)
    except Exception as e:
        raise ValueError(f"{Colors.RED}ERROR: {Colors.RESET}{e}")
    
    print(
        f"{Colors.GREEN}SUCCESS: {Colors.RESET}"
        "Configuration file successfully analyzed."
    )

    return {
        ConfigOptions.WIDTH: config.width,
        ConfigOptions.HEIGHT: config.height,
        ConfigOptions.ENTRY: config.entry,
        ConfigOptions.EXIT: config.exit,
        ConfigOptions.OUTPUT_FILE: config.output_file,
        ConfigOptions.PERFECT: config.perfect,
        ConfigOptions.FORTYTWO: config.fortytwo
    }