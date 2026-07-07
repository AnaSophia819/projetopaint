from modelo.figuras import Desenho, Linha, Retangulo, Oval, Poligono, MaoLivre

class ControladorPaint:
    def __init__(self):
        
        self.modelo_desenho = Desenho()
        self.visao_interface = None

        self.ferramenta_atual = "Linha"
        self.cor_borda = "black"
        self.cor_preenchimento = ""

        self.inicio_x = None
        self.inicio_y = None

        self.coordenadas_atuais = []
        self.pontos_poligono = []
        self.figura_atual = None

        self.classes_figuras = {"Linha": Linha, "Retângulo": Retangulo, "Oval": Oval, "Polígono": Poligono, "Mão livre": MaoLivre}

    def definir_visao(self, visao):
            self.visao_interface = visao

    def mudar_ferramenta(self, ferramenta):
        self.ferramenta_atual = ferramenta
        self.encerra_poligono()

    def atualizar_cor_borda(self, cor):
        self.cor_borda = cor

    def atualizar_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor

    # LÓGICA DO MOUSE 
  
    def inicia_desenho(self, event):
        self.inicio_x = event.x
        self.inicio_y = event.y
        self.figura_atual = None

        if self.ferramenta_atual == "Polígono":
            self.pontos_poligono.extend([event.x, event.y])
            self.visao_interface.canvas.delete("temporario")
            
            if len(self.pontos_poligono) >= 6:
                self.figura_atual = Poligono(self.pontos_poligono, self.cor_borda, self.cor_preenchimento)
                self.visao_interface.renderizar_figura(self.figura_atual)
        else:
            self.coordenadas_atuais = [event.x, event.y]

    def atualiza_desenho(self, event):
        if self.ferramenta_atual == "Polígono":
            return

        self.visao_interface.canvas.delete("temporario")
        ferramenta = self.ferramenta_atual

        if ferramenta == "Mão livre":
            self.coordenadas_atuais.extend([event.x, event.y])
            self.figura_atual = MaoLivre(self.coordenadas_atuais, self.cor_borda)
        else:
            ClasseFigura = self.classes_figuras[ferramenta]
            self.figura_atual = ClasseFigura(
                self.inicio_x, self.inicio_y, event.x, event.y, 
                self.cor_borda, self.cor_preenchimento
            )

        if self.figura_atual:
            self.figura_atual.desenhar(self.visao_interface.canvas, tags="temporario")

    def finaliza_desenho(self, event):
        if self.ferramenta_atual != "Polígono":
            self.visao_interface.canvas.dtag("temporario", "figura_definitiva")
            if self.figura_atual:
                self.modelo_desenho.adicionar_figuras(self.figura_atual)
            self.figura_atual = None

    def encerra_poligono(self, event=None):
        if self.pontos_poligono:
            self.visao_interface.canvas.dtag("temporario", "figura_definitiva")
            if self.figura_atual:
                self.modelo_desenho.adicionar_figuras(self.figura_atual)
            self.pontos_poligono = []
            self.figura_atual = None
