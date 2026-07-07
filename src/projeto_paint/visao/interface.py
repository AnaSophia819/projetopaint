import tkinter as tk
from tkinter import ttk
from tkinter import ttk, colorchooser
from modelo.figuras import Linha, Retangulo, Oval, Poligono, MaoLivre

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
        self.btn_borda = ttk.Button(self.painel, text="Cor da Borda", command=self.escolher_borda)
        self.btn_borda.grid(row=0, column=2, padx=5, pady=5)
        self.btn_fundo = ttk.Button(self.painel, text="Cor do Fundo", command=self.escolher_preenchimento)
        self.btn_fundo.grid(row=0, column=3, padx=5, pady=5)
    #A tela que o usuario vai utilizar para desenhar
        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack()
        self.canvas.bind('<ButtonPress-1>', self.controlador.inicia_desenho) #as ações do mouse na tela e passa as informções para o controlador
        self.canvas.bind('<B1-Motion>', self.controlador.atualiza_desenho)
        self.canvas.bind('<ButtonRelease-1>', self.controlador.finaliza_desenho)
        self.canvas.bind('<ButtonPress-3>', self.controlador.encerra_poligono) #botão direito do mouse

#metodo que liga o controlador e o canvas
    # Abre a janela de cor e manda o resultado pro controlador
    def escolher_borda(self):
        cor = colorchooser.askcolor(title="Cor da Borda")[1]
        if cor: self.controlador.atualizar_cor_borda(cor)

    def escolher_preenchimento(self):
        cor = colorchooser.askcolor(title="Cor do Preenchimento")[1]
        if cor: self.controlador.atualizar_cor_preenchimento(cor)

    # O Método que pega a "casca vazia" do Modelo e joga na tela (O Controlador pede isso)
    def renderizar_figura(self, figura, tag="temporario"):
        if isinstance(figura, Linha):
            self.canvas.create_line(figura.x1, figura.y1, figura.x2, figura.y2, fill=figura.cor_borda, tags=tag)
        elif isinstance(figura, Retangulo):
            self.canvas.create_rectangle(figura.x1, figura.y1, figura.x2, figura.y2, outline=figura.cor_borda, fill=figura.cor_preenchimento, tags=tag)
        elif isinstance(figura, Oval):
            self.canvas.create_oval(figura.x1, figura.y1, figura.x2, figura.y2, outline=figura.cor_borda, fill=figura.cor_preenchimento, tags=tag)
        elif isinstance(figura, Poligono):
            self.canvas.create_polygon(figura.coordenadas, outline=figura.cor_borda, fill=figura.cor_preenchimento, tags=tag)
        elif isinstance(figura, MaoLivre):
            self.canvas.create_line(figura.coordenadas, fill=figura.cor_borda, tags=tag)