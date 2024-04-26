CAN_LEFT = {'─', '┐', '┘', '┤', '┬', '┴', '┼', 'J', 'q', '-', '2', '3', '6', '10'}
CAN_RIGHT = {'─', '┌', '└', '├', '┬', '┴', '┼', 'p', 'L', '-', '4', '5', '6', '12'}
CAN_UP = {'│', '└', '┘', '├', '┤', '┴', '┼', 'J', 'L', '|', '1', '3', '5', '9'}
CAN_DOWN = {'│', '┌', '┐', '├', '┤', '┬', '┼', 'q', 'p', '|'}


class Maze:
  def __init__(self, buffer):
    self.buffer = buffer
    self.width = len(buffer)
    self.height = len(buffer[0])
  
  def printWall(self):
    toWall = [' ', '╵', '╴', '┘', '╶', '└', '─', '┴', '╷', '│', '┐', '┤', '┌', '├', '┬', '┼']
    res = [[" " for j in range(2*self.height+1)] for i in range(2*self.width+1)]

    for i in range(2*self.width+1):
      for j in range(2*self.height+1):
        if i % 2 == 0 and j % 2 == 0:
          res[i][j] = "#"
        elif i % 2 == 0:
          res[i][j] = "─"
        elif j % 2 == 0:
          res[i][j] = "│"

    res[0][2*self.height] = '┐'
    res[2*self.width][0] = '└'
    for i in range(1, 2*self.width, 2):
      for j in range(1, 2*self.height, 2):
        c = self.buffer[i//2][j//2]
        if c & 2: res[i][j-1] = " "
        if c & 4: res[i][j+1] = " "
        if c & 1: res[i-1][j] = " "
        if c & 8: res[i+1][j] = " "
    
    for i in range(0, 2*self.width+1, 2):
      for j in range(0, 2*self.height+1, 2):
        som = 0
        if i > 0 and res[i-1][j] != " ": som += 1
        if j > 0 and res[i][j-1] != " ": som += 2
        if i < 2*self.width-1 and res[i+1][j] != " ": som += 8
        if j < 2*self.height-1 and res[i][j+1] != " ": som += 4
        res[i][j] = toWall[som]

    print("\n".join(["".join(res[i]) for i in range(2*self.width+1)]))
  
  def printPath(self):
    # toPath = [' ', '╵', '╴', '┘', '╶', '└', '─', '┴', '╷', '│', '┐', '┤', '┌', '├', '┬', '┼']
    # toPath = [' ', '│', '─', '┘', '─', '└', '─', '┴', '│', '│', '┐', '┤', '┌', '├', '┬', '┼']
    toPath = [' ', '║', '═', '╝', '═', '╚', '═', '╩', '║', '║', '╗', '╣', '╔', '╠', '╦', '╬']
    res = [[toPath[int(self.buffer[i][j])] for j in range(self.height)] for i in range(self.width)]
    print("\n".join(["".join(res[i]) for i in range(self.width)]))
