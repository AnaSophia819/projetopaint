import tkinter as tk
from tkinter import ttk

#responsavel por toda a parte visual do paint (cria a tela, botões). Repassa o que o usuario escolheu  para o controlador
class Interface:
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("Mini Paint")
        self.controlador = controlador
        self.painel = tk.Frame(self.root)  #painel
        self.painel.pack(pady=5)
        tk.Label(self.painel, text="Ferramenta:").grid(row=0, column=0, padx=5, pady=5)

    #criando o combobox e iniciando a ferramenta linha para o usuario
        self.cb_ferramenta = ttk.Combobox(self.painel, values=["Linha", "Retângulo", "Oval", "Polígono", "Mão livre"], state="readonly")
        self.cb_ferramenta.set("Linha") 
        self.cb_ferramenta.grid(row=0, column=1, padx=5, pady=5)
    #aqui serve para passar a informação para o controlador do que o usuario escolheu
        self.cb_ferramenta.bind("<<ComboboxSelected>>", lambda e: self.controlador.mudar_ferramenta(self.cb_ferramenta.get()))
    #botões de cores (avisam o controlador quando clicados)
        self.btn_borda = ttk.Button(self.painel, text="Cor da Borda", command=self.controlador.escolher_borda)
        self.btn_borda.grid(row=0, column=2, padx=5, pady=5)
        self.btn_fundo = ttk.Button(self.painel, text="Cor do Fundo", command=self.controlador.escolher_preenchimento)
        self.btn_fundo.grid(row=0, column=3, padx=5, pady=5)
    #A tela que o usuario vai utilizar para desenhar
        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack()
        self.canvas.bind('<ButtonPress-1>', self.controlador.inicia_desenho) #as ações do mouse na tela e passa as informções para o controlador
        self.canvas.bind('<B1-Motion>', self.controlador.atualiza_desenho)
        self.canvas.bind('<ButtonRelease-1>', self.controlador.finaliza_desenho)
        self.canvas.bind('<ButtonPress-3>', self.controlador.encerra_poligono) #botão direito do mouse

#metodo que liga o controlador e o canvas
    def obter_canvas(self):
        return self.canvas