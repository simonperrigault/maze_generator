import tkinter as tk
from collections import deque

COULEUR_MUR = "black"
COULEUR_SOL = "white"
COULEUR_SOLUTION = "red"
PERIODE_ANIM = 5
WALL_WIDTH = 2

class MazeDisplay:
  def __init__(self, buffer, anim, solution):
    self.buffer = buffer
    self.width = len(buffer)
    self.height = len(buffer[0])

    self.anim = anim
    self.solution = solution

    self.taille_carreau = 20

    self.fenetre = tk.Tk()
    self.fwidth = self.taille_carreau*self.height
    self.fheight = self.taille_carreau*self.width
    self.fenetre.geometry(f"{self.fwidth}x{self.fheight}")
    self.curr_anim = 0

    # self.taille_carreau = min(self.fwidth//self.mheight, self.fheight//self.mwidth)
    
    self.canvas = tk.Canvas(self.fenetre, background=COULEUR_MUR)
    self.canvas.pack(expand=True, fill="both")

    #self.dessiner_carte()
    self.animer_carte()
    self.afficher_solution()

    self.fenetre.mainloop()

  def dessiner_carte(self):
    for i in range(self.width):
      for j in range(self.height):
        self.colorier_carreau(i,j)
  
  def animer_carte(self):
    for i,j in self.anim:
      self.colorier_carreau(i,j,self.curr_anim)
      self.curr_anim += 1

  def afficher_solution(self):
    for i in range(len(self.solution)):
      x1, y1 = self.solution[i]
      self.colorier_carreau(x1, y1, self.curr_anim, COULEUR_SOLUTION)
      self.curr_anim += 1

  def colorier_carreau(self, i, j, k=0, couleur=COULEUR_SOL):
    haut = i*self.taille_carreau
    gauche = j*self.taille_carreau
    bas = (i+1)*self.taille_carreau
    droite = (j+1)*self.taille_carreau
    self.canvas.after(k*PERIODE_ANIM, lambda : self.canvas.create_rectangle(gauche, haut, droite, bas, fill=couleur, width=0))
    c = self.buffer[i][j]
    if not c & 1: self.canvas.after(k*PERIODE_ANIM, lambda : self.canvas.create_line(gauche-WALL_WIDTH//2, haut, droite+WALL_WIDTH//2, haut, fill=COULEUR_MUR, width=WALL_WIDTH))
    if not c & 2: self.canvas.after(k*PERIODE_ANIM, lambda : self.canvas.create_line(gauche, haut-WALL_WIDTH//2, gauche, bas+WALL_WIDTH//2, fill=COULEUR_MUR, width=WALL_WIDTH))
    if not c & 4: self.canvas.after(k*PERIODE_ANIM, lambda : self.canvas.create_line(droite, bas+WALL_WIDTH//2, droite, haut-WALL_WIDTH//2, fill=COULEUR_MUR, width=WALL_WIDTH))
    if not c & 8: self.canvas.after(k*PERIODE_ANIM, lambda : self.canvas.create_line(gauche-WALL_WIDTH//2, bas, droite+WALL_WIDTH//2, bas, fill=COULEUR_MUR, width=WALL_WIDTH))