import tkinter as tk
from tkinter import colorchooser

corDaBorda = "black"

def escolher_cor_borda():
    global corDaBorda

    cor_escolhida = colorchooser.askcolor(title="Escolha a cor da borda")

    if cor_escolhida[1] is not None:
        corDaBorda = cor_escolhida[1]

inicio_x = None 
inicio_y = None
fim_x = None
fim_y = None

# Quando o mouse é pressionado
def inicia_desenho(event):
    global inicio_x, inicio_y
    inicio_x = event.x
    inicio_y = event.y

# Quando o mouse é movido com o botão pressionado (Efeito "Draft")
def atualiza_desenho(event):
    global fim_x, fim_y
    fim_x = event.x      
    fim_y = event.y
    
    # Apaga o desenho temporário anterior para não criar um rastro
    canvas.delete("temporario") 

    # Cria a linha e coloca a tag "temporario" nela
    canvas.create_line(inicio_x, inicio_y, fim_x, fim_y, fill=corDaBorda, tags="temporario")

# Quando o mouse é solto, o desenho se torna permanente
def finaliza_desenho(event):
    # Remove a tag "temporario" do último objeto desenhado para que ele não seja apagado no próximo clique
    canvas.dtag("temporario", "temporario")
    # (O que procurar, o que apagar)

# Configuração da janela principal
root = tk.Tk()
root.title("Mini Paint")

# Configuração do Canvas
canvas = tk.Canvas(root, bg='white', width=600, height=600)
canvas.pack()

painel_botoes = tk.Frame(root)
painel_botoes.pack()

bt_borda = tk.Button(painel_botoes, text="Borda", command=escolher_cor_borda)
bt_borda.pack(side=tk.LEFT, padx=10)


# Vínculos (Bindings) de eventos do mouse
canvas.bind('<ButtonPress-1>', inicia_desenho)
canvas.bind('<B1-Motion>', atualiza_desenho)
canvas.bind('<ButtonRelease-1>', finaliza_desenho)

root.mainloop()