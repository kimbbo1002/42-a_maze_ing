_This project has been created as part of the 42 curriculum by \<bokim> and \<yghergho>_.

# A-MAZE-ING

## Description
- A Python-based maze generation and navigation tool that utilizes the Depth-First Search (DFS) algorithm. This project was developed to demonstrate modular Python design, stack-based logic, and terminal-based visualization.

- Overview: This application generates a randomized maze and solves it using a stack-based DFS approach. It focuses on clean, importable code and provides a real-time visual representation of the pathfinding process directly in your terminal.

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
---

### Usage Instructions
#### Installation
To get started, install the virtual environment and all required dependencies using:
```bash
make install
```

#### Running the Program
After setup, you can generate and display a maze with:
```bash
make run
```
⚠️ Make sure to provide a `config_file.txt` before running.

The maze will appear directly in your terminal. Interactive controls allow you to:
- Change colors
- Generate a new maze
- Toggle the solution path (entry → exit)
- Quit the program

#### Debug Mode
To run the project with Python’s built-in debugger (`pdb`), use:
```bash
make debug
```
The program will pause at the first line, letting you step through execution interactively.

Common `pdb` commands:
- `n` — execute the next line
- `s` — step into a function
- `c` — continue execution
- `q` — quit the debugger

#### Build the Package
To generate a `.whl` package for reuse, run:
```bash
make build
```
The built package will be placed at the root of the repository.

#### Linting
To check code quality and ensure compliance with flake8 and type hints:
```bash
make lint
```
For stricter validation:
```bash
make lint-strict
```

#### Cleaning the Project
Remove cache and temporary files with:
```bash
make clean
```
To fully reset the project (removes generated files such as `.lock`, `.tar`, `.whl`, `output.txt`, and `dist`):
```bash
make fclean
```

## Technical Implementation 
For this project, our team implemented the Depth-First Search (DFS) algorithm, specifically utilizing an iterative approach with explicit stacks.

### Depth-First Search (DFS)
DFS is a graph traversal algorithm that explores as far as possible along each branch before backtracking. In the context of maze generation, it functions as a "randomized backtracker," carving out paths by moving to unvisited neighbors until it hits a dead end, then retreating to the last cell with available options.

### Using DFS with Stacks
While DFS is often taught using recursion, we chose to implement it using an explicit stack data structure (`stack = []`).
- **Iterative Control**: By using a while loop and a stack, we manually manage the history of the path.
- **Benefits vs. Recursion**: * Avoiding Stack Overflow: Python has a default recursion limit (usually 1000). For large mazes, a recursive DFS would crash. Our stack-based approach allows for significantly larger maze dimensions.
  - **Memory Efficiency**: We have more granular control over memory allocation and state management compared to the overhead of multiple function calls.

### Maze Generation Logic
Our `generate_maze` method in the `Maze` class creates a "perfect" maze (no loops, all areas reachable):
1. **Initialization**: Sets the entry and exit points and calculates a `target` cell count (excluding any pre-defined patterns like the "42" pattern).

2. **Traversal**: Starting from the entry, the algorithm randomly selects an unvisited neighbor.

3. **Wall Removal**: When moving to a new cell, the `remove_walls` method breaks the barrier between the current and next cell to create a passage.

4. **Backtracking**: If a cell has no unvisited neighbors, the algorithm `pops` from the stack to backtrack to a previous cell and continue the search until all `target` cells are visited.

### Maze Solving Logic
The `get_path` method in the `Maze` class finds the solution from entry to exit:
1. **Pathfinding**: It uses a stack to explore the passages. Because we check if not current.walls[wall], the algorithm is restricted to the paths carved during the generation phase.

2. **Back-Pointer Mapping**: We use a visited dictionary ({next: current}) to store where we came from. This allows us to "retrace our steps" once the exit is reached.

3. **Path Reconstruction**: Once the exit is found, the algorithm crawls backward through the visited map to flag the correct path and converts the cell-to-cell movement into directional strings ('N', 'S', 'E', 'W').

### Code Reusability & Standalone Integration
This project is built following modular programming principles. The core logic is decoupled from the execution script, allowing the maze generation and solving capabilities to be imported into any future Python project (e.g., a game, a pathfinding visualizer, or a robotics simulation).

#### The Standalone Module: `MazeGenerator`
The MazeGenerator class acts as a high-level wrapper that manages the lifecycle of a maze. It is "standalone" because it encapsulates all necessary dependencies—parsing, seeding, generation, and solving—into a single, portable interface.

**What makes it reusable:**
- **Encapsulation**: All algorithmic complexity (DFS stack logic) is hidden. Users only interact with the generate_maze() method
- **Input Flexibility**: It accepts a seed for reproducibility but can also function entirely autonomously.
- **Object-Oriented Design**: The generator returns a Maze object, providing structured access to the grid and path data rather than just printing text.

#### How to Reuse This Module
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

## Project Management
### Roles
This project was a collaborative effort with a clear division of responsibilities:
- **bokim**: Lead for Logic & Parsing.
  - Developed the **DFS Algorithm** and stack-based solver.
  - Authored the technical **documentation** and package structure.

- **yghergho**: Lead for Visualization & Workflow.
  - Developed the **terminal-based visual representation**.
  - Developed the **Makefile** for automated execution.
  
### Plan Evolvement
The project was strategically divided into two distinct phases: Algorithm Development and UI Visualization.
- **Execution**: The roadmap was followed as intended, beginning with the core logic implementation, followed by the integration of the terminal interface.

- **Knowledge** Transfer: Once the technical milestones were reached, we prioritized cross-team communication. This ensured that both contributors gained a comprehensive understanding of the entire codebase—bridging the gap between the back-end logic and the front-end display.

- **Outcome**: This phased approach led to a successful, stable implementation where the final product aligned perfectly with our initial design goals.

### Future Improvements
While the core functionality is stable, the following features were deferred due to time constraints. We believe these additions will significantly enhance the package's versatility and user experience:
- **Expanded Algorithm Library**: Support for additional generation methods (such as BFS) to provide different maze patterns and complexities.
- **Real-Time Animation**: Implementation of a frame-by-frame rendering mode to visualize the generation process as it happens, rather than just the final result.

### Tool usage
To ensure the project is scalable, type-safe, and easy to distribute, we integrated the following industry-standard tools:
- **Pydantic**: Utilized for robust data validation and parsing. This ensures that maze dimensions and configuration inputs adhere to strict schemas, preventing runtime errors.

- **Pynput**: Integrated to handle real-time user input, allowing for interactive control and navigation within the terminal visualization.

- **Poetry**: Employed for dependency management and packaging. This allows other developers to install the project and its requirements with a single command, ensuring a consistent environment across different machines.

## Resources
- [DFS Algorithm](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/)
- Maze generation:
  - [Maze Generator](https://inventwithpython.com/recursion/chapter11.html)
  - [Maze creation in Python](https://discuss.python.org/t/maze-creation-in-python/77030)
### Use of AI
- Concept clarification and simplification
- Debugging assistance
- Documentation (README) drafting and refinement