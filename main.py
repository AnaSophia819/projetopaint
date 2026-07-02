import tkinter as tk
from tkinter import colorchooser
from figuras import Linha, Oval, Retangulo, Poligono, MaoLivre

class MiniPaint:

    def __init__(self, root):
        
        self.root = root
        self.root.title("Mini Paint")

        # Figura que começa
        self.ferramenta_atual = "linha"
        self.cor_borda = "black"
        self.cor_preenchimento = ""

        # Coordenadas iniciais
        self.in_x = None
        self.in_y = None

        # Meio que um dicionário de classes 
        self.classes_figuras = {"Linha": Linha, "Retângulo": Retangulo, "Oval": Oval, "Polígono": Poligono, "Mão livre": MaoLivre}

        # Criação do painel
        self.painel = tk.Frame(self.root)
        self.painel.pack(pady=5)

        # Criação do botao para escolher a borda
        self.btn_borda = tk.Button(self.painel, text="Cor Borda", command=self.escolher_borda)
        self.btn_borda.pack(side=tk.LEFT, padx=5)

        # Criação do botao para escolher a cor de preenchimento
        self.btn_fundo = tk.Button(self.painel, text="Cor Preenchimento", command=self.escolher_preenchimento)
        self.btn_fundo.pack(side=tk.LEFT, padx=5)

        # Botões para mudar de ferramenta (término com as classes das figuras feitas)
        
        self.btn_lin = tk.Button(self.painel, text="Linha", command=lambda: self.mudar_ferramenta("Linha"))
        self.btn_lin.pack(side=tk.LEFT, padx=5)

        self.btn_ret = tk.Button(self.painel, text="Retângulo", command=lambda: self.mudar_ferramenta("Retângulo"))
        self.btn_ret.pack(side=tk.LEFT, padx=5)
        
        self.btn_ova = tk.Button(self.painel, text="Oval", command=lambda: self.mudar_ferramenta("Oval"))
        self.btn_ova.pack(side=tk.LEFT, padx=5)

        self.btn_pol = tk.Button(self.painel, text="Polígono", command=lambda: self.mudar_ferramenta("Polígono"))
        self.btn_pol.pack(side=tk.LEFT, padx=5)

        self.btn_mao = tk.Button(self.painel, text="Mão livre", command=lambda: self.mudar_ferramenta("Mão livre"))
        self.btn_mao.pack(side=tk.LEFT, padx=5)


        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack()


        # Botões
        self.canvas.bind('<ButtonPress-1>', self.inicia_desenho)
        self.canvas.bind('<B1-Motion>', self.atualiza_desenho)
        self.canvas.bind('<ButtonRelease-1>', self.finaliza_desenho)
