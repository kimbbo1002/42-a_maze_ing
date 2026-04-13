# MAZEGEN

## How to Reuse This Module
To integrate this into a different project, ensure the module is in your path and use the following implementation:
1. Basic Example (Instantiating & Running)
```python
from maze_module import MazeGenerator

# Create the generator instance
# The seed is optional; if omitted, a random one is generated.
gen = MazeGenerator(seed=123)

# The generate_maze() method handles config, generation, and solving
maze_instance = gen.generate_maze()
```

2. Accessing the Generated Structure
Once generated, you can programmatically access the maze's internal structure for your own needs:
```python
# Access the raw grid (list of Cell objects)
cells = maze_instance.grid_cells

# Check wall status of a specific cell (e.g., the entry cell)
print(cells[0].walls) # Returns {'N': True, 'S': False, ...}
```

3. Accessing the Solution
The solution is pre-calculated and stored within the returned object:
```python
# Access the solution path as a list of directions
print(f"Solution Path: {maze_instance.path}") 
# Output example: ['E', 'S', 'E', 'N', 'E']
```

## Instructions
### Configuration File Instructions
The application uses a simple key-value configuration file to define parameters. Each setting must be written on a separate line using the following format:
```bash
KEY=VALUE
```
#### Example
```bash
WIDTH=21
HEIGHT=15
ENTRY=0,0
EXIT=20,14
OUTPUT_FILE=output.txt
PERFECT=True
```

#### Parameters
- WIDTH

The width of the grid or maze. Must be a positive integer.
- HEIGHT

The height of the grid or maze. Must be a positive integer.
- ENTRY

The starting position, defined as x,y coordinates.
Example: 0,0
- EXIT

The ending position, defined as x,y coordinates.
Example: 20,14
- OUTPUT_FILE

The name (or path) of the file where the result will be saved.
- PERFECT

A boolean value (`True` or `False`).
  - `True`: Generates a perfect maze (no loops, exactly one path between any two points).
  - `False`: Allows multiple paths and loops.

#### Notes
- Variable names are **case-insensitive** (e.g., width, Width, and WIDTH are all valid).
- Boolean values for PERFECT can be written as true or false (case-insensitive).
- Coordinates must always be within the bounds defined by WIDTH and HEIGHT.
- Whitespace around keys and values is ignored.