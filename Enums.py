from enum import Enum

class Colors:
    RED = '\033[91m'
    GREEN = "\033[0;32m"
    RESET = '\033[0m'

class ConfigOptions(Enum):
    WIDTH = 'WIDTH'
    HEIGHT = 'HEIGHT'
    ENTRY = 'ENTRY'
    EXIT = 'EXIT'
    OUTPUT_FILE = 'OUTPUT_FILE'
    PERFECT = 'PERFECT'