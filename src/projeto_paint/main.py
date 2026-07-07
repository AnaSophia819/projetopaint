import tkinter as tk
from visao.interface import Interface
from controlador.app_controller import ControladorPaint

if __name__ == "__main__":
    root = tk.Tk()
    
    # 1. Cria o Controlador (Cérebro)
    controlador = ControladorPaint()
    
    # 2. Cria a Tela (Visão) e informa quem é o Controlador
    app = Interface(root, controlador)
    
    # 3. Informa ao Controlador quem é a Tela
    controlador.definir_visao(app)
    
    root.mainloop()