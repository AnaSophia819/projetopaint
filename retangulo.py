import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

corDaBorda = "black"

def escolher_cor_borda():
    global corDaBorda

    cor_escolhida = colorchooser.askcolor(title="Escolha a cor da borda")

    if cor_escolhida[1] is not None:
        corDaBorda = cor_escolhida[1]

def iniciar_figura_nova(event):
    global figura_nova

    if tipo_figura_var.get() == "Retângulo":
        figura_nova = [event.x, event.y, event.x, event.y]
        
def atualizar_figura_nova(event):
    global figura_nova

    if tipo_figura_var.get() == "Retângulo":
        if figura_nova:
            canvas.delete("temporário")
            figura_nova[2] = event.x
            figura_nova[3] = event.y
            canvas.create_rectangle(figura_nova[0], figura_nova[1], figura_nova[2], figura_nova[3], tags = "temporário", outline= corDaBorda)

def finalizar_figura(event):
    global figura_nova

    if tipo_figura_var.get() == "Retângulo":
        if figura_nova:
            canvas.itemconfig("temporário", tags = "figura")
            figuras.append(figura_nova)
            figura_nova = None

def main():
    global canvas, tipo_figura_var
    
    painel = tk.Tk()
    frame = tk.Frame(painel)
    canvas = tk.Canvas(frame, background = "white", width = 600, height = 600)
    canvas.grid(column = 0, row = 1, columnspan = 2, sticky = tk.W)
    tipo_figura_var = tk.StringVar(painel)
    menu_de_opcoes = ttk.OptionMenu(frame, tipo_figura_var, "Retângulo", "Retângulo")
    menu_de_opcoes.grid(column = 1, row = 0, sticky = tk.W)

    canvas.bind("<Button-1>", iniciar_figura_nova)
    canvas.bind("<B1-Motion>", atualizar_figura_nova)
    canvas.bind("<ButtonRelease-1>", finalizar_figura)

    painel_botoes = tk.Frame(painel) # Cria o painel para ficar os botões
    painel_botoes.pack()

    bt_borda = tk.Button(painel_botoes, text="Borda", command=escolher_cor_borda) # Cria o botão
    bt_borda.pack(side=tk.LEFT, padx=10)

    frame.pack()
    painel.mainloop()

figuras = []
figura_nova = None

main()