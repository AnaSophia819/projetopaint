from modelo.figuras import Desenho, Linha, Retangulo, Oval, Poligono, MaoLivre


class EstadoFerramenta:
    def __init__(self, ctrl): self.ctrl = ctrl
    def inicia(self, event): pass
    def atualiza(self, event): pass
    def finaliza(self, event): pass
    def encerra(self): pass

# Controla o desenho de Linha, Retângulo e Oval 
class EstadoForma2Pontos(EstadoFerramenta):
    def __init__(self, ctrl, classe_figura):
        super().__init__(ctrl)
        self.classe = classe_figura

    def inicia(self, e):
        # Salva o ponto inicial e cria a figura temporária
        self.ctrl.inicio_x, self.ctrl.inicio_y = e.x, e.y
        self.ctrl.figura_atual = self.classe(e.x, e.y, e.x, e.y, self.ctrl.cor_borda, self.ctrl.cor_preenchimento)

    def atualiza(self, e):
        # Atualiza o ponto  enquanto o mouse é arrastado
        self.ctrl.visao_interface.canvas.delete("temporario")
        if self.ctrl.figura_atual:
            self.ctrl.figura_atual.x2, self.ctrl.figura_atual.y2 = e.x, e.y
            self.ctrl.figura_atual.desenhar(self.ctrl.visao_interface.canvas, tags="temporario")

    def finaliza(self, e):
        # Salva a figura definitiva ao soltar o botão do mouse 
        self.ctrl.visao_interface.canvas.dtag("temporario", "figura_definitiva")
        if self.ctrl.figura_atual:
            self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)
        self.ctrl.figura_atual = None

# Controla o traço contínuo e as direções 
class EstadoMaoLivre(EstadoFerramenta):
    def inicia(self, e):
        
        self.ctrl.coordenad as_atuais = [e.x, e.y]
        self.ctrl.figura_atual = None

    def atualiza(self, e):
        # Adiciona novos pontos à lista ao arrastar o mouse
        self.ctrl.visao_interface.canvas.delete("temporario")
        self.ctrl.coordenadas_atuais.extend([e.x, e.y])
        self.ctrl.figura_atual = MaoLivre(self.ctrl.coordenadas_atuais, self.ctrl.cor_borda)
        self.ctrl.figura_atual.desenhar(self.ctrl.visao_interface.canvas, tags="temporario")

    def finaliza(self, e):
        # Salva o traço definitivo ao soltar o clique
        self.ctrl.visao_interface.canvas.dtag("temporario", "figura_definitiva")
        if self.ctrl.figura_atual:
            self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)

class EstadoPoligono(EstadoFerramenta):
    def inicia(self, e):
        # Adiciona coordenadas a cada clique e desenha a partir de 3 pontos 
        self.ctrl.pontos_poligono.extend([e.x, e.y])
        self.ctrl.visao_interface.canvas.delete("temporario")
        if len(self.ctrl.pontos_poligono) >= 6:
            self.ctrl.figura_atual = Poligono(self.ctrl.pontos_poligono, self.ctrl.cor_borda, self.ctrl.cor_preenchimento)
            self.ctrl.figura_atual.desenhar(self.ctrl.visao_interface.canvas, tags="temporario")

    def encerra(self):
        # Fecha e salva o polígono ao trocar de ferramenta ou encerrar manualmente
        if self.ctrl.pontos_poligono:
            self.ctrl.visao_interface.canvas.dtag("temporario", "figura_definitiva")
            if self.ctrl.figura_atual:
                self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)
            self.ctrl.pontos_poligono = []
            self.ctrl.figura_atual = None


class ControladorPaint:
    def __init__(self):
        self.modelo_desenho = Desenho()
        self.visao_interface = None
        self.cor_borda = "black"
        self.cor_preenchimento = ""
        self.inicio_x = None
        self.inicio_y = None
        self.coordenadas_atuais = []
        self.pontos_poligono = []
        self.figura_atual = None
        
        # Define o estado inicial
        self.estado_atual = EstadoForma2Pontos(self, Linha)

    def definir_visao(self, visao):
        self.visao_interface = visao

    def mudar_ferramenta(self, ferramenta):
        # Fecha polígonos abertos antes de trocar de ferramenta
        self.estado_atual.encerra()
        
               mapa_estados = {
            "Linha": EstadoForma2Pontos(self, Linha),
            "Retângulo": EstadoForma2Pontos(self, Retangulo),
            "Oval": EstadoForma2Pontos(self, Oval),
            "Mão livre": EstadoMaoLivre(self),
            "Polígono": EstadoPoligono(self)
        }
        self.estado_atual = mapa_estados[ferramenta]

    def atualizar_cor_borda(self, cor):
        self.cor_borda = cor

    def atualizar_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor

  
    # LÓGICA DO MOUSE 
    
    def inicia_desenho(self, event):
        self.estado_atual.inicia(event)

    def atualiza_desenho(self, event):
        self.estado_atual.atualiza(event)

    def finaliza_desenho(self, event):
        self.estado_atual.finaliza(event)

    def encerra_poligono(self, event=None):
        if hasattr(self.estado_atual, 'encerra'):
            self.estado_atual.encerra()
