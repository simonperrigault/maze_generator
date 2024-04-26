import tkinter as tk
from collections import deque

COULEUR_MUR = "black"
COULEUR_SOL = "white"
COULEUR_SOLUTION = "red"
PERIODE_ANIM = 5

class MazeDisplay:
  def __init__(self, buffer, anim, solution):
    self.buffer = buffer
    self.width = len(buffer)
    self.height = len(buffer[0])
    self.mwidth = 2*self.width-1
    self.mheight = 2*self.height-1

    self.anim = anim
    self.solution = solution

    self.map = [[0 for j in range(self.mheight)] for i in range(self.mwidth)]
    for i in range(0, self.mwidth, 2):
      for j in range(0, self.mheight, 2):
        self.map[i][j] = 1
        c = self.buffer[i//2][j//2]
        if c & 2: self.map[i][j-1] = 1
        if c & 4: self.map[i][j+1] = 1
        if c & 1: self.map[i-1][j] = 1
        if c & 8: self.map[i+1][j] = 1

    self.taille_carreau = 10 if self.width <= 50 and self.height <= 90 else 5

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
    for i in range(len(self.solution)-1):
      x1, y1 = self.solution[i]
      x2, y2 = self.solution[i+1]
      dx, dy = x2-x1, y2-y1
      self.colorier_carreau(2*x1, 2*y1, self.curr_anim, COULEUR_SOLUTION)
      self.colorier_carreau(2*x1+dx, 2*y1+dy, self.curr_anim, COULEUR_SOLUTION)
      self.curr_anim += 1
    self.colorier_carreau(self.mwidth-1, self.mheight-1, self.curr_anim, COULEUR_SOLUTION)


  def colorier_carreau(self, i, j, k=0, couleur=COULEUR_SOL):
    haut_gauche = (j*self.taille_carreau, i*self.taille_carreau)
    bas_droite = ((j+1)*self.taille_carreau, (i+1)*self.taille_carreau)
    self.canvas.after(k*PERIODE_ANIM, lambda : self.canvas.create_rectangle(haut_gauche, bas_droite, fill=couleur, width=0))
  
  