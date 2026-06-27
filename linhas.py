import tkinter as tk

# Variáveis de estado
desenho = "retangulo"  # Pode ser "retangulo" ou "linha"
corDaBorda = "blue"
corPreenchimento = "yellow"

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

    if desenho == "linha":
        canvas.create_line(inicio_x, inicio_y, fim_x, fim_y, fill=corDaBorda, tags="temporario")
    elif desenho == "retangulo":
        canvas.create_rectangle(inicio_x, inicio_y, fim_x, fim_y, outline=corDaBorda, fill=corPreenchimento, tags="temporario")

# Quando o mouse é solto, o desenho se torna permanente
def finaliza_desenho(event):
    # Remove a tag "temporario" do último objeto desenhado para que ele não seja apagado no próximo clique
    canvas.dtag("temporario", "temporario")

# Configuração da janela principal
root = tk.Tk()
root.title("Mini Paint")

# Configuração do Canvas
canvas = tk.Canvas(root, bg='white', width=600, height=600)
canvas.pack()

# Vínculos (Bindings) de eventos do mouse
canvas.bind('<ButtonPress-1>', inicia_desenho)
canvas.bind('<B1-Motion>', atualiza_desenho)
canvas.bind('<ButtonRelease-1>', finaliza_desenho)

root.mainloop()