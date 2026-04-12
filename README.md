_This project has been created as part of the 42 curriculum by \<bokim> and \<yghergho>_.

## Description
- A Python-based maze generation and navigation tool that utilizes the Depth-First Search (DFS) algorithm. This project was developed to demonstrate modular Python design, stack-based logic, and terminal-based visualization.

- Overview: This application generates a randomized maze and solves it using a stack-based DFS approach. It focuses on clean, importable code and provides a real-time visual representation of the pathfinding process directly in your terminal.

## Instructions

To start, run the following command to install a virtual environment using poetry and create all dependencies needed
```
make install
``` 

<br>

Once everything is set up, run this command to generate the maze and display it (you must provide a ```config_file.txt```)
```
make run
```
*The maze will be displayed on your terminal with an available render control allowing you to switch colors, re-generate a new maze, show/hide the path from entry to exit or quit.*

<br>

To run the project in debug mode using Python's built-in debugger (`pdb`), run:

```bash
make debug
```

*The program will pause at the first line, allowing you to step through the code interactively.*

*Useful `pdb` commands:*
- *`n` — execute the next line*
- *`s` — step into a function*
- *`c` — continue until the next breakpoint*
- *`q` — quit the debugger*

<br>

The following rule will build the package `.whl` for module reusability as specified in the subject and place it at the root of the repository
```
make build
```
<br>

If you want to check wether the project respects the flake8 norm and ensures consistent type hints across the codebase, run this
```
make lint
```
*or this for strict checks*
```
make lint-strict
```

<br>

In order to clean the project from cache directories, run this command
```
make clean
```

*or this one to reset it to its original state, removing virtual environment as well as files/directories generated during the process (`.lock`, `.tar`, `.whl`, `output.txt`, `dist`)*
```
make fclean
```
<br>

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
### Use of AI
- Concept clarification and simplification
- Debugging assistance
- Documentation (README) drafting and refinement