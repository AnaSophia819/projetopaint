# Desenha apenas uma linha
# Ao desenhar outra, apaga a anterior

import tkinter as tk
from tkinter import colorchooser

corDaBorda = "black"

def escolher_cor_borda():
    global corDaBorda

    cor_escolhida = colorchooser.askcolor(title="Escolha a cor da borda")

    if cor_escolhida[1] is not None:
        corDaBorda = cor_escolhida[1]


def marca_inicio(event):
    global ini_x, ini_y
    ini_x = event.x
    ini_y = event.y

def atualiza_fim(event):
    global fim_x, fim_y
    fim_x = event.x
    fim_y = event.y
    canvas.delete("all")
    canvas.create_line(ini_x, ini_y, fim_x, fim_y, fill=corDaBorda)


root = tk.Tk()

canvas = tk.Canvas(root, bg='white', width=600, height=600)
canvas.pack()

painel_botoes = tk.Frame(root) # Cria o painel
painel_botoes.pack() # Socorro, como coloca isso pra cima?

bt_borda = tk.Button(painel_botoes, text= "Borda", command=escolher_cor_borda)
bt_borda.pack(side=tk.LEFT, padx=10)


ini_x = None  # coordenadas do ponto inicial da linha
ini_y = None
fim_x = None
fim_y = None
canvas.bind('<ButtonPress-1>', marca_inicio)
canvas.bind('<B1-Motion>', atualiza_fim)
#canvas.bind('<ButtonRelease-1>', reset)

root.mainloop()