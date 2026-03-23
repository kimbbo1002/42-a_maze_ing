from pydantic import Basemodel, field_validator, model_validator
from typing import List

class Config(Basemodel):
    width: int
    height: int
    entry: List[int]
    exit: List[int]
    output_file: str
    perfect: bool

    @field_validator("width", "height")
    def check_width_height(cls, value):
        if value <= 0:
            raise ValueError("Width and Height must be positive.")
        return value
    
    @field_validator("output_file")
    def check_outputfile(cls, value):
        if not value.strip().endswith(".txt"):
            raise ValueError("Output file must be a .txt file.")
        return value
    
    @model_validator(mode="after")
    def check_maze_logic(self):
        width, height = self.width, self.height
        entry, exit = self.entry, self.exit
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("Entry coordinates out of bounds.")
        if not (0 <= exit[0] < width and 0 <= exit[1] < height):
            raise ValueError("Exit coordinates out of bounds.")
        if entry == exit:
            raise ValueError("Entry and Exit cannot be the same.")
        return self


def check_config() -> Config:
    raw = {}
    