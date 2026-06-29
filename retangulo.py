import tkinter
from tkinter import ttk

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
            canvas.create_rectangle(figura_nova[0], figura_nova[1], figura_nova[2], figura_nova[3], tags = "temporário")

def finalizar_figura(event):
    global figura_nova

    if tipo_figura_var.get() == "Retângulo":
        if figura_nova:
            canvas.itemconfig("temporário", tags = "figura")
            figuras.append(figura_nova)
            figura_nova = None

def main():
    global canvas, tipo_figura_var
    
    painel = tkinter.Tk()
    frame = tkinter.Frame(painel)
    canvas = tkinter.Canvas(frame, background = "white", width = 600, height = 600)
    canvas.grid(column = 0, row = 1, columnspan = 2, sticky = tkinter.W)
    tipo_figura_var = tkinter.StringVar(painel)
    menu_de_opcoes = ttk.OptionMenu(frame, tipo_figura_var, "Retângulo", "Retângulo")
    menu_de_opcoes.grid(column = 1, row = 0, sticky = tkinter.W)

    canvas.bind("<Button-1>", iniciar_figura_nova)
    canvas.bind("<B1-Motion>", atualizar_figura_nova)
    canvas.bind("<ButtonRelease-1>", finalizar_figura)

    frame.pack()
    painel.mainloop()

figuras = []
figura_nova = None

main()