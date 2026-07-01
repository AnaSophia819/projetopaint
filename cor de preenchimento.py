import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

cor_interior = ""

def escolher_cor_preenchimento():
    global cor_interior
    cor = colorchooser.askcolor(title="Escolha a cor de preenchimento")
    
    if cor[1]:
        cor_interior = cor[1]
    else:
        cor_interior = ""
        
if desenho == "retangulo":
    canvas.create_rectangle(x1, y1, x2, y2, fill=cor_preench, outline=cor)
elif desenho == "oval":
    canvas.create_oval(x1, y1, x2, y2, fill=cor_preench, outline=cor)

button_preenchimento = ttk.Button(frame, text="Cor de Preenchimento", command=escolher_cor_preenchimento)
button_preenchimento.grid(column=0, row=2, columnspan=3, padx=5, pady=5)
