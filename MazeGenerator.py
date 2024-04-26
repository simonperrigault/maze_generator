from random import randint, choice
from collections import deque

DIR = [(-1, 0), (1, 0), (0, 1), (0, -1)]
DIR_TO_CODE = {
  (-1, 0) : 1,
  (1, 0) : 8,
  (0, -1) : 2,
  (0, 1) : 4
}

class MazeGenerator:
  @staticmethod
  def randomDFS(width, height):
    res = [[0 for j in range(height)] for i in range(width)]

    anim = deque()
    stack = deque()
    stack.append((randint(0, width-1), randint(0, height-1)))
    anim.append(stack[0])

    while stack:
      x, y = stack[-1]
      if MazeGenerator.hasNext(res, x, y):
        dx, dy = choice(DIR)
        if not 0 <= x+dx < width or not 0 <= y+dy < height: continue
        if not res[x+dx][y+dy]:
          stack.append((x+dx, y+dy))
          anim.append(stack[-1])
          res[x][y] += DIR_TO_CODE[(dx, dy)]
          res[x+dx][y+dy] += DIR_TO_CODE[(-dx, -dy)]

      else:
        stack.pop()
    
    # res[0][0] |= 2
    # res[width-1][height-1] |= 4

    return res, anim
  
  @staticmethod
  def randomPrim(width, height):
    res = [[0 for j in range(height)] for i in range(width)]

    anim = deque()
    walls = list()
    x, y = randint(0, width-1), randint(0, height-1)
    for dir in range(4):
      walls.append((x, y, dir))
    anim.append((x,y))

    while walls:
      iwall = randint(0, len(walls)-1)
      x, y, idir = walls[iwall]
      walls.pop(iwall)
      dx, dy = DIR[idir]
      if not 0 <= x+dx < width or not 0 <= y+dy < height: continue
      if res[x+dx][y+dy]: continue
      anim.append((x+dx, y+dy))
      res[x][y] += DIR_TO_CODE[(dx, dy)]
      res[x+dx][y+dy] += DIR_TO_CODE[(-dx, -dy)]
      for dir in range(4):
        if dir == idir: continue
        walls.append((x+dx, y+dy, dir))

    return res, anim
  
  @staticmethod
  def aldousbroder(width, height):
    res = [[0 for j in range(height)] for i in range(width)]

    anim = deque()
    x, y = randint(0, width-1), randint(0, height-1)
    anim.append((x,y))
    visited = 1

    while visited < width*height:
      dx, dy = choice(DIR)
      if not 0 <= x+dx < width or not 0 <= y+dy < height: continue
      if not res[x+dx][y+dy]:
        res[x][y] += DIR_TO_CODE[(dx, dy)]
        res[x+dx][y+dy] += DIR_TO_CODE[(-dx, -dy)]
        visited += 1
        anim.append((x+dx, y+dy))
      x, y = x+dx, y+dy

    return res, anim
  
  @staticmethod
  def wilson(width, height):
    res = [[0 for j in range(height)] for i in range(width)]

    anim = deque()
    visited = [[False for j in range(height)] for i in range(width)]
    visited[randint(0, width-1)][randint(0, height-1)] = True
    visited_count = 1

    while visited_count < width*height:
      xstart, ystart = randint(0, width-1), randint(0, height-1)
      while visited[xstart][ystart]:
        xstart, ystart = randint(0, width-1), randint(0, height-1)
      exit = [[None for j in range(height)] for i in range(width)]
      x, y = xstart, ystart
      while not visited[x][y]:
        dx, dy = choice(DIR)
        if not 0 <= x+dx < width or not 0 <= y+dy < height: continue
        exit[x][y] = (dx, dy)
        x, y = x+dx, y+dy

      x, y = xstart, ystart
      while not visited[x][y]:
        next_x, next_y = x+exit[x][y][0], y+exit[x][y][1]
        dx = next_x - x
        dy = next_y - y
        res[x][y] += DIR_TO_CODE[(dx, dy)]
        res[next_x][next_y] += DIR_TO_CODE[(-dx, -dy)]
        visited[x][y] = True
        visited_count += 1
        anim.append((x, y))
        x, y = next_x, next_y

    return res, anim
  
  @staticmethod
  def hasNext(grid, i, j):
    width, height = len(grid), len(grid[0])
    if i > 0 and not grid[i-1][j]: return True
    if j > 0 and not grid[i][j-1]: return True
    if i < width-1 and not grid[i+1][j]: return True
    if j < height-1 and not grid[i][j+1]: return True
    return False
