import tkinter as tk
from collections import deque
import time

COULEUR_MUR = "black"
COULEUR_SOL = "white"
COULEUR_SOLUTION = "red"
PERIODE_ANIM = 5
MARGIN = 5
TEMPS_INITIAL_ANIM = 1000
OFFSET_RETARD = 40

class MazeDisplay4:
  def __init__(self, buffer1, anim1, solu1, buffer2, anim2, solu2, buffer3, anim3, solu3, buffer4, anim4, solu4):
    self.buffers = [buffer1, buffer2, buffer3, buffer4]
    self.width = len(buffer1)
    self.height = len(buffer1[0])
    self.mwidth = 2*self.width-1
    self.mheight = 2*self.height-1

    self.retard = 0

    self.anims = [anim1, anim2, anim3, anim4]
    self.solus = [solu1, solu2, solu3, solu4]

    self.maps = [[[0 for _ in range(self.mheight)] for _ in range(self.mwidth)] for _ in range(4)]
    for k in range(4):
      for i in range(0, self.mwidth, 2):
        for j in range(0, self.mheight, 2):
          self.maps[k][i][j] = 1
          c = self.buffers[k][i//2][j//2]
          if c & 2: self.maps[k][i][j-1] = 1
          if c & 4: self.maps[k][i][j+1] = 1
          if c & 1: self.maps[k][i-1][j] = 1
          if c & 8: self.maps[k][i+1][j] = 1

    self.taille_carreau = 6

    self.fenetre = tk.Tk()
    self.fwidth = self.taille_carreau*self.mheight*2
    self.fheight = self.taille_carreau*self.mwidth*2
    self.fenetre.geometry(f"{self.fwidth+5*MARGIN}x{self.fheight+5*MARGIN}")
    self.curr_anim = TEMPS_INITIAL_ANIM

    # self.taille_carreau = min(self.fwidth//self.mheight, self.fheight//self.mwidth)

    self.canvas = [tk.Canvas(self.fenetre, background=COULEUR_MUR) for _ in range(4)]
    for i in range(4):
      self.canvas[i].configure(width=self.fwidth//2, height=self.fheight//2)
      self.canvas[i].grid(row=i//2, column=i%2, padx=MARGIN, pady=MARGIN)

    for i in range(4):
      self.animer_carte(i)
      self.afficher_solution(i)
      self.curr_anim = TEMPS_INITIAL_ANIM - self.retard

    self.fenetre.mainloop()
  
  def animer_carte(self, k):
    debut = time.time()
    for i,j in self.anims[k]:
      i *= 2
      j *= 2
      self.colorier_carreau(k,i,j,self.curr_anim)
      c = self.buffers[k][i//2][j//2]
      if c & 2: self.colorier_carreau(k,i,j-1,self.curr_anim)
      if c & 4: self.colorier_carreau(k,i,j+1,self.curr_anim)
      if c & 1: self.colorier_carreau(k,i-1,j,self.curr_anim)
      if c & 8: self.colorier_carreau(k,i+1,j,self.curr_anim)
      self.curr_anim += 1
    self.retard += int(time.time() - debut)+OFFSET_RETARD

  def afficher_solution(self, k):
    debut = time.time()
    for i in range(len(self.solus[k])-1):
      x1, y1 = self.solus[k][i]
      x2, y2 = self.solus[k][i+1]
      dx, dy = x2-x1, y2-y1
      self.colorier_carreau(k, 2*x1, 2*y1, self.curr_anim, COULEUR_SOLUTION)
      self.colorier_carreau(k, 2*x1+dx, 2*y1+dy, self.curr_anim, COULEUR_SOLUTION)
      self.curr_anim += 1
    self.colorier_carreau(k, self.mwidth-1, self.mheight-1, self.curr_anim, COULEUR_SOLUTION)
    self.retard += int(time.time() - debut)+OFFSET_RETARD
    


  def colorier_carreau(self, k, i, j, time=0, couleur=COULEUR_SOL):
    haut_gauche = (j*self.taille_carreau, i*self.taille_carreau)
    bas_droite = ((j+1)*self.taille_carreau, (i+1)*self.taille_carreau)
    self.canvas[k].after(time*PERIODE_ANIM, lambda : self.canvas[k].create_rectangle(haut_gauche, bas_droite, fill=couleur, width=0))
  
  @staticmethod
  def code_to_dir(code):
    res = []
    if code & 1: res.append((-1, 0))
    if code & 2: res.append((0, -1))
    if code & 4: res.append((0, 1))
    if code & 8: res.append((1, 0))
    return res