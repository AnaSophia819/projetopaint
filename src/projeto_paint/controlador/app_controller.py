from modelo.figuras import Desenho, Linha, Retangulo, Oval

class ControladorPaint:
    def __init__(self):
        
        self.modelo_desenho = Desenho()
        self.visao_interface = None

        self.ferramenta_atual = "linha"
        self.cor_borda = "black"
        self.corpreenchimento = ""

        self.inicio_x = None
        self.inicio_y = None

        self.classes_figuras = {"linha": Linha, "retangulo": Retangulo, "oval": Oval}

        def definir_visao(self, visao):
            self.visao_interface = visao

        def mudar_ferramenta(self, ferramenta):
            self.ferramenta_atual = ferramenta
        
        def cor_borda(self):
            # Fazer a parte no visor para ter algo para colocar aqui.