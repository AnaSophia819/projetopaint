import tkinter as tk
from tkinter import colorchooser

#ajuda com o gemini para a lógica com o tkinter

root = tk.Tk()
canvas = tk.Canvas(root, bg='white', width=600, height=600)
canvas.pack() # Empacotar o canvas para ele aparecer na janela
corDaBorda = "black" # Começa com a cor preta 

def escolher_cor_borda(): # Função para escolher a cor
    global corDaBorda

    cor_escolhida = colorchooser.askcolor(title="Escolha a cor da borda")

    if cor_escolhida[1] is not None:
        corDaBorda = cor_escolhida[1]


def marcar_inicio(event):
    global inicial_x, inicial_y, id_oval
    inicial_x = event.x
    inicial_y = event.y

    id_oval = canvas.create_oval(inicial_x, inicial_y, inicial_x, inicial_y, outline= corDaBorda)

def atualiza_linha(event):
    global atual_x, atual_y
    atual_x = event.x
    atual_y = event.y

    canvas.coords(id_oval, inicial_x, inicial_y, atual_x, atual_y )

painel_botoes = tk.Frame(root) # Cria o painel para ficar os botões
painel_botoes.pack()

bt_borda = tk.Button(painel_botoes, text="Borda", command=escolher_cor_borda) # Cria o botão
bt_borda.pack(side=tk.LEFT, padx=10)

canvas.bind("<Button-1>", marcar_inicio)
canvas.bind("<B1-Motion>", atualiza_linha)

root.mainloop()