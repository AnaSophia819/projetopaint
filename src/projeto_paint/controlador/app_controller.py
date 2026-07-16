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
        self.ctrl.visao_interface.canvas.itemconfig("temporario", tags="figura_definitiva")
        if self.ctrl.figura_atual:
            self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)
        self.ctrl.figura_atual = None

# Controla o traço contínuo e as direções 
class EstadoMaoLivre(EstadoFerramenta):
    def inicia(self, e):
        self.ctrl.coordenadas_atuais = [e.x, e.y]
        self.ctrl.figura_atual = None

    def atualiza(self, e):
        # Adiciona novos pontos à lista ao arrastar o mouse
        self.ctrl.visao_interface.canvas.delete("temporario")
        self.ctrl.coordenadas_atuais.extend([e.x, e.y])
        self.ctrl.figura_atual = MaoLivre(self.ctrl.coordenadas_atuais, self.ctrl.cor_borda)
        self.ctrl.figura_atual.desenhar(self.ctrl.visao_interface.canvas, tags="temporario")

    def finaliza(self, e):
        # Salva o traço definitivo ao soltar o clique
        self.ctrl.visao_interface.canvas.itemconfig("temporario", tags="figura_definitiva")
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
            self.ctrl.visao_interface.canvas.itemconfig("temporario", tags="figura_definitiva")
            if self.ctrl.figura_atual:
                self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)
            self.ctrl.pontos_poligono = []
            self.ctrl.figura_atual = None

class EstadoSelecionar(EstadoFerramenta):
    def inicia(self, e):
        
        shift_pressionado = (e.state & 1) != 0

        if not shift_pressionado:
            self.ctrl.figuras_selecionadas.clear()

        self.x_inicio = e.x
        self.y_inicio = e.y

        self.id_caixa = self.ctrl.visao_interface.canvas.create_rectangle(self.x_inicio, self.y_inicio, self.x_inicio, self.y_inicio, dash=(4, 4), outline="blue", tags="caixa_selecao")

    def atualiza(self, e):

        self.ctrl.visao_interface.canvas.coords(self.id_caixa, self.x_inicio, self.y_inicio, e.x, e.y)

    def finaliza(self, e):
        canvas = self.ctrl.visao_interface.canvas

        x1 = min(self.x_inicio, e.x)
        y1 = min(self.y_inicio, e.y)
        x2 = max(self.x_inicio, e.x)
        y2 = max(self.y_inicio, e.y)

        canvas.delete(self.id_caixa)
       
        if abs(x2 - x1) < 3 and abs(y2 - y1) < 3:
            itens_encontrados = canvas.find_withtag("current")
        else:
            itens_encontrados = canvas.find_overlapping(x1, y1, x2, y2)

        if itens_encontrados:
            for id_item in itens_encontrados:
                for figura in self.ctrl.modelo_desenho.figuras:
                    if hasattr(figura, 'id_tk') and figura.id_tk == id_item:
                        if figura not in self.ctrl.figuras_selecionadas:
                            self.ctrl.figuras_selecionadas.append(figura)
                            print(f"[+] Selecionou a figura: {figura.__class__.__name__}")
                        break
        else:
            shift_pressionado = (e.state & 1) != 0
             
            if not shift_pressionado:
                self.ctrl.figuras_selecionadas.clear()
                print("Clicou no vazio. Seleção limpa.")

        print(f"Total de selecionadas: {len(self.ctrl.figuras_selecionadas)}")



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
        self.figuras_selecionadas = []
        
        # Define o estado inicial
        self.estado_atual = EstadoForma2Pontos(self, Linha)

    def definir_visao(self, visao):
        self.visao_interface = visao

    def mudar_ferramenta(self, ferramenta):
        # Fecha polígonos abertos antes de trocar de ferramenta
        self.estado_atual.encerra()
        
        mapa_estados = {
            "Selecionar": EstadoSelecionar(self),
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
