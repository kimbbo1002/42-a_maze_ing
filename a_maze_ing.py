import sys
from typing import Dict, Any
from Enums import ConfigOptions
from Parsing_config import check_config


def main() -> None:
    try:
        config = check_config()
        print(config)
    except Exception as e:
        print(e)

main()