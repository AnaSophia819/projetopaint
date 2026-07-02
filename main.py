import tkinter as tk
from tkinter import colorchooser
from figuras import Linha, MaoLivre, Oval, Retangulo 

class MiniPaint:

    def __init__(self, root):
        
        self.root = root
        self.root.title("Mini Paint")

        # Figura que começa
        self.ferramenta_atual = "linha"
        self.cor_borda = "black"
        self.cor_preenchimento = ""

        # Coordenadas iniciais
        self.inicio_x = None
        self.inicio_y = None

        # Meio que um dicionário de classes 
        self.classes_figuras = {"linha": Linha, "maolivre": MaoLivre, "oval": Oval, "retangulo": Retangulo,  }

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
        self.btn_ret = tk.Button(self.painel, text="Retângulo", command=lambda: self.mudar_ferramenta("retangulo"))
        self.btn_ret.pack(side=tk.LEFT, padx=5)
        self.btn_lin = tk.Button(self.painel, text="Linha", command=lambda: self.mudar_ferramenta("linha"))
        self.btn_lin.pack(side=tk.LEFT, padx=5)
        self.btn_mao = tk.Button(self.painel, text="Mão Livre", command=lambda: self.mudar_ferramenta("maolivre"))
        self.btn_mao.pack(side=tk.LEFT, padx=5)
        self.btn_ova = tk.Button(self.painel, text="Oval", command=lambda: self.mudar_ferramenta("oval"))
        self.btn_ova.pack(side=tk.LEFT, padx=5)


        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack()


        # Botões
        self.canvas.bind('<ButtonPress-1>', self.inicia_desenho)
        self.canvas.bind('<B1-Motion>', self.atualiza_desenho)
        self.canvas.bind('<ButtonRelease-1>', self.finaliza_desenho)

    # Métodos de Cor e Ferramenta
    def escolher_borda(self):
        cor = colorchooser.askcolor(title="Cor da Borda")
        if cor[1]: self.cor_borda = cor[1]

    def escolher_preenchimento(self):
        cor = colorchooser.askcolor(title="Cor do Preenchimento")
        if cor[1]: self.cor_preenchimento = cor[1]

    def mudar_ferramenta(self, ferramenta):
        self.ferramenta_atual = ferramenta

    #Lógica de Eventos do Mouse
    def inicia_desenho(self, event):
        self.inicio_x = event.x
        self.inicio_y = event.y

        ClasseFigura = self.classes_figuras[self.ferramenta_atual]
        self.figura_atual = ClasseFigura(self.inicio_x, self.inicio_y, event.x, event.y, 
                                         self.cor_borda, self.cor_preenchimento)

    def atualiza_desenho(self, event):
        self.canvas.delete("temporario")

        #usa o método de adicionar pontos para rabiscos
        if self.ferramenta_atual == "maolivre":
            self.figura_atual.adicionar_ponto(event.x, event.y)
        #se for outra figura só muda as coordenadas finais
        else:
            self.figura_atual.x2 = event.x
            self.figura_atual.y2 = event.y
        
        #Desenho da figura de forma autonoma
        self.figura_atual.desenhar(self.canvas, tags="temporario")

    def finaliza_desenho(self, event):
        self.canvas.dtag("temporario", "temporario")

# Inicialização do programa
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniPaint(root)
    root.mainloop()
