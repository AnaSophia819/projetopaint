import tkinter as tk
from tkinter import colorchooser

class Figura:
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def desenhar(self, canvas, tags=""):
        raise NotADirectoryError()
    

class Linha(Figura):
    def desenhar(self, canvas, tags=""):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, tags= "linha")