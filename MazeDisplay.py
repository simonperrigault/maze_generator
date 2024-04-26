import tkinter as tk
from collections import deque

COULEUR_MUR = "black"
COULEUR_SOL = "white"
COULEUR_SOLUTION = "red"
PERIODE_ANIM = 5

class MazeDisplay:
  def __init__(self, buffer, anim):
    self.buffer = buffer
    self.width = len(buffer)
    self.height = len(buffer[0])
    self.mwidth = 2*self.width-1
    self.mheight = 2*self.height-1

    self.anim = anim

    self.map = [[0 for j in range(self.mheight)] for i in range(self.mwidth)]
    for i in range(0, self.mwidth, 2):
      for j in range(0, self.mheight, 2):
        self.map[i][j] = 1
        c = self.buffer[i//2][j//2]
        if c & 2: self.map[i][j-1] = 1
        if c & 4: self.map[i][j+1] = 1
        if c & 1: self.map[i-1][j] = 1
        if c & 8: self.map[i+1][j] = 1

    self.taille_carreau = 10

    self.fenetre = tk.Tk()
    self.fwidth = self.taille_carreau*self.mheight
    self.fheight = self.taille_carreau*self.mwidth
    self.fenetre.geometry(f"{self.fwidth}x{self.fheight}")
    self.curr_anim = 0

    # self.taille_carreau = min(self.fwidth//self.mheight, self.fheight//self.mwidth)
    
    self.canvas = tk.Canvas(self.fenetre, background=COULEUR_MUR)
    self.canvas.pack(expand=True, fill="both")

    # self.dessiner_carte()
    self.animer_carte()
    self.afficher_solution()

    self.fenetre.mainloop()

  def dessiner_carte(self):
    for i in range(self.mwidth):
      for j in range(self.mheight):
        if self.map[i][j]:
          self.colorier_carreau(i,j)
  
  def animer_carte(self):
    for i,j in self.anim:
      i *= 2
      j *= 2
      self.colorier_carreau(i,j,self.curr_anim)
      c = self.buffer[i//2][j//2]
      if c & 2: self.colorier_carreau(i,j-1,self.curr_anim)
      if c & 4: self.colorier_carreau(i,j+1,self.curr_anim)
      if c & 1: self.colorier_carreau(i-1,j,self.curr_anim)
      if c & 8: self.colorier_carreau(i+1,j,self.curr_anim)
      self.curr_anim += 1

  def afficher_solution(self):
    queue = deque()
    queue.append((0,0))
    prece = [[None for j in range(self.height)] for i in range(self.width)]
    while queue:
      x, y = queue.popleft()
      for dx, dy in MazeDisplay.code_to_dir(self.buffer[x][y]):
        if not prece[x+dx][y+dy]:
          prece[x+dx][y+dy] = (x, y)
          queue.append((x+dx, y+dy))
    x, y = self.width-1, self.height-1
    self.colorier_carreau(2*x, 2*y, self.curr_anim, COULEUR_SOLUTION)
    while (x, y) != (0, 0):
      prev_x, prev_y = prece[x][y]
      dx = x - prev_x
      dy = y - prev_y
      self.colorier_carreau(2*x - dx, 2*y - dy, self.curr_anim, COULEUR_SOLUTION)
      self.colorier_carreau(2*x, 2*y, self.curr_anim, COULEUR_SOLUTION)
      x, y = prev_x, prev_y
      self.curr_anim += 1
    self.colorier_carreau(0, 0, self.curr_anim, COULEUR_SOLUTION)
    


  def colorier_carreau(self, i, j, k=0, couleur=COULEUR_SOL):
    haut_gauche = (j*self.taille_carreau, i*self.taille_carreau)
    bas_droite = ((j+1)*self.taille_carreau, (i+1)*self.taille_carreau)
    self.canvas.after(k*PERIODE_ANIM, lambda : self.canvas.create_rectangle(haut_gauche, bas_droite, fill=couleur, width=0))
  
  @staticmethod
  def code_to_dir(code):
    res = []
    if code & 1: res.append((-1, 0))
    if code & 2: res.append((0, -1))
    if code & 4: res.append((0, 1))
    if code & 8: res.append((1, 0))
    return res