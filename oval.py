import tkinter as tk
from tkinter import ttk

#ajuda com o gemini para a lógica com o tkinter

root = tk.Tk()
canvas = tk.Canvas(root, bg='white', width=600, height=600)
canvas.pack() #empacotar o canvas para ele aparecer na janela

def marcar_inicio(event):
    global inicial_x, inicial_y, id_oval
    inicial_x = event.x
    inicial_y = event.y

    id_oval = canvas.create_oval(inicial_x, inicial_y, inicial_x, inicial_y, outline="black")

def atualiza_linha(event):
    global atual_x, atual_y
    atual_x = event.x
    atual_y = event.y

    canvas.coords(id_oval, inicial_x, inicial_y, atual_x, atual_y )

canvas.bind("<Button-1>", marcar_inicio)
canvas.bind("<B1-Motion>", atualiza_linha)

root.mainloop()