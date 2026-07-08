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

  
    # NOVA LÓGICA DO MOUSE 
    
    def inicia_desenho(self, event):
        self.estado_atual.inicia(event)

    def atualiza_desenho(self, event):
        self.estado_atual.atualiza(event)

    def finaliza_desenho(self, event):
        self.estado_atual.finaliza(event)

    def encerra_poligono(self, event=None):
        if hasattr(self.estado_atual, 'encerra'):
            self.estado_atual.encerra()
