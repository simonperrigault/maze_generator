from Maze import Maze
from MazeGenerator import MazeGenerator
from MazeDisplay import MazeDisplay
import sys

filepath = "maze.txt"

if len(sys.argv) > 1:
  method = sys.argv[1]
  width = int(sys.argv[2])
  height = int(sys.argv[3])
  if method == "dfs":
    maze, anim = MazeGenerator.randomDFS(width, height)
  elif method == "prim":
    maze, anim = MazeGenerator.randomPrim(width, height)
  elif method == "aldousbroder":
    maze, anim = MazeGenerator.aldousbroder(width, height)
  elif method == "wilson":
    maze, anim = MazeGenerator.wilson(width, height)
  else:
    print("Invalid method")
    sys.exit(1)

  display = MazeDisplay(maze, anim)
