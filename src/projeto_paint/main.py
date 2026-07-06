import tkinter as tk
from tkinter import colorchooser
from figuras import Linha, Oval

class MiniPaint:

    def __init__(self, root):
        
        self.root = root
        self.root.title("Mini Paint")

        # Figura que começa
        self.ferramenta_atual = "Linha"
        self.cor_borda = "black"
        self.cor_preenchimento = ""

        # Coordenadas iniciais
        self.inicio_x = None
        self.inicio_y = None

        # Meio que um dicionário de classes 
        self.classes_figuras = {"Linha": Linha, "Oval": Oval, "Retângulo": Retangulo, "Polígono": Poligono, "Mão livre": MaoLivre}

        # Criação do painel
        self.painel = tk.Frame(self.root)
        self.painel.pack(pady=5)

        # Criação do botao para escolher a borda
   
        tk.Label(self.painel, text="Ferramenta:").grid(row=0, column=0, padx=5, pady=5)
        
        self.cb_ferramenta = ttk.Combobox(self.painel, values=["Linha", "Retângulo", "Oval", "Polígono", "Mão livre"], state="readonly")
        self.cb_ferramenta.set("Linha") 
        self.cb_ferramenta.grid(row=0, column=1, padx=5, pady=5)
        
        self.cb_ferramenta.bind("<<ComboboxSelected>>", lambda e: self.mudar_ferramenta(self.cb_ferramenta.get()))

        self.btn_borda = ttk.Button(self.painel, text="Cor da Borda", command=self.escolher_borda)
        self.btn_borda.grid(row=0, column=2, padx=5, pady=5)

        self.btn_fundo = ttk.Button(self.painel, text="Cor do Fundo", command=self.escolher_preenchimento)
        self.btn_fundo.grid(row=0, column=3, padx=5, pady=5)
        


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
        self.coordenadas_atuais = [event.x, event.y]
        self.figura_atual = None

    def atualiza_desenho(self, event):
        self.canvas.delete("temporario")
        
        ferramenta = self.ferramenta_atual

        # Formas de múltiplos pontos
        if ferramenta in ["Polígono", "Mão livre"]:
            self.coordenadas_atuais.extend([event.x, event.y])
            
            if ferramenta == "Polígono":
                self.figura_atual = Poligono(self.coordenadas_atuais, self.cor_borda, self.cor_preenchimento)
            else:
                self.figura_atual = MaoLivre(self.coordenadas_atuais, self.cor_borda)
                
        # Formas de 2 pontos (Linha, Retângulo, Oval)
        else:
            ClasseFigura = self.classes_figuras[ferramenta]
            self.figura_atual = ClasseFigura(
                self.inicio_x, self.inicio_y, event.x, event.y, 
                self.cor_borda, self.cor_preenchimento
            )

        if self.figura_atual:
            self.figura_atual.desenhar(self.canvas, tags="temporario")

    def finaliza_desenho(self, event):
        self.canvas.dtag("temporario", "temporario")
        self.figura_atual = None

# Inicialização do programa
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniPaint(root)
    root.mainloop()
