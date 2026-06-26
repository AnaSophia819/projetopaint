import tkinter as tk
from tkinter import ttk


figuras = []        
def main():
    global canvas, cor_contorno_var, cor_preenchimento_var

    root = tk.Tk()
    frame = tk.Frame(root)
    paddings = {'padx': 5, 'pady': 5}

    
    ttk.Label(frame, text='Contorno:').grid(column=0, row=0, sticky=tk.W, **paddings)
    cor_contorno_var = tk.StringVar(root)
    ttk.OptionMenu(frame, cor_contorno_var, 'black', 'black', 'red', 'blue', 'green').grid(column=1, row=0, **paddings)

    
    ttk.Label(frame, text='Preenchimento:').grid(column=2, row=0, sticky=tk.W, **paddings)
    cor_preenchimento_var = tk.StringVar(root)
    ttk.OptionMenu(frame, cor_preenchimento_var, 'Nenhum', 'Nenhum', 'yellow', 'red', 'blue', 'green').grid(column=3, row=0, **paddings)

    
    canvas = tk.Canvas(frame, bg='white', width=600, height=600)
    canvas.grid(column=0, row=1, columnspan=4, sticky=tk.W, **paddings)
    frame.pack()

    

    root.mainloop()

if __name__ == "__main__":
    main()