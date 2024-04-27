from Maze import Maze
from MazeGenerator import MazeGenerator
from MazeDisplay import MazeDisplay
from MazeDisplay4 import MazeDisplay4
import sys

filepath = "maze.txt"

if len(sys.argv) > 1:
  method = sys.argv[1]
  if method == "-4":
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    if width >= 50 or height >= 50:
      print("Width and height must be less than 50")
      sys.exit(1)
    MazeDisplay4(*MazeGenerator.dfs(width, height), *MazeGenerator.prim(width, height), *MazeGenerator.aldousbroder(width, height), *MazeGenerator.wilson(width, height))
  else:
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    if method == "dfs":
      maze, anim, solution = MazeGenerator.dfs(width, height)
    elif method == "prim":
      maze, anim, solution = MazeGenerator.prim(width, height)
    elif method == "aldousbroder":
      maze, anim, solution = MazeGenerator.aldousbroder(width, height)
    elif method == "wilson":
      maze, anim, solution = MazeGenerator.wilson(width, height)
    else:
      print("Invalid method")
      sys.exit(1)
    display = MazeDisplay(maze, anim, solution)
