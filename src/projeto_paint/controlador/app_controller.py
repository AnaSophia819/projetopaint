from modelo.figuras import Desenho, Linha, Retangulo, Oval, Poligono, MaoLivre, FiguraComposta

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
        self.ctrl.inicio_x, self.ctrl.inicio_y = e.x, e.y
        self.ctrl.figura_atual = self.classe(e.x, e.y, e.x, e.y, self.ctrl.cor_borda, self.ctrl.cor_preenchimento)

    def atualiza(self, e):
        self.ctrl.visao_interface.canvas.delete("temporario")
        if self.ctrl.figura_atual:
            self.ctrl.figura_atual.x2, self.ctrl.figura_atual.y2 = e.x, e.y
            self.ctrl.visao_interface.renderizar_figura(self.ctrl.figura_atual, tag="temporario")

    def finaliza(self, e):
        if self.ctrl.figura_atual:
            itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
            if itens_temporarios:
                id_gerado = itens_temporarios[-1]
                self.ctrl.figura_atual.id_tk = id_gerado 
                self.ctrl.visao_interface.canvas.itemconfig(id_gerado, tags="figura_definitiva")
                self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)
        self.ctrl.figura_atual = None

# Controla o traço contínuo e as direções 
class EstadoMaoLivre(EstadoFerramenta):
    def inicia(self, e):
        self.ctrl.coordenadas_atuais = [e.x, e.y]
        self.ctrl.figura_atual = None

    def atualiza(self, e):
        self.ctrl.visao_interface.canvas.delete("temporario")
        self.ctrl.coordenadas_atuais.extend([e.x, e.y])
        self.ctrl.figura_atual = MaoLivre(self.ctrl.coordenadas_atuais, self.ctrl.cor_borda)
        self.ctrl.visao_interface.renderizar_figura(self.ctrl.figura_atual, tag="temporario")

    def finaliza(self, e):
        if self.ctrl.figura_atual:
            itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
            if itens_temporarios:
                id_gerado = itens_temporarios[-1]
                self.ctrl.figura_atual.id_tk = id_gerado 
                self.ctrl.visao_interface.canvas.itemconfig(id_gerado, tags="figura_definitiva")
                self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)
        self.ctrl.figura_atual = None

class EstadoPoligono(EstadoFerramenta):
    def inicia(self, e):
        self.ctrl.pontos_poligono.extend([e.x, e.y])
        self.ctrl.visao_interface.canvas.delete("temporario")
        if len(self.ctrl.pontos_poligono) >= 6:
            self.ctrl.figura_atual = Poligono(self.ctrl.pontos_poligono, self.ctrl.cor_borda, self.ctrl.cor_preenchimento)
            self.ctrl.visao_interface.renderizar_figura(self.ctrl.figura_atual, tag="temporario")

    def encerra(self):
        if self.ctrl.pontos_poligono:
            if self.ctrl.figura_atual:
                itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
                if itens_temporarios:
                    id_gerado = itens_temporarios[-1]
                    self.ctrl.figura_atual.id_tk = id_gerado
                    self.ctrl.visao_interface.canvas.itemconfig(id_gerado, tags="figura_definitiva")
                    self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)
            self.ctrl.pontos_poligono = []
            self.ctrl.figura_atual = None

class EstadoSelecionar(EstadoFerramenta):
    def inicia(self, e):
        self.modo_mover = False
        self.x_inicio = e.x
        self.y_inicio = e.y
        self.ultimo_x = e.x
        self.ultimo_y = e.y

        itens_clicados = self.ctrl.visao_interface.canvas.find_overlapping(e.x - 1, e.y - 1, e.x + 1, e.y + 1)
        
        figura_clicada = None
        if itens_clicados:
            for id_clicado in reversed(itens_clicados):
                # Busca recursivamente nas figuras (para achar itens agrupados)
                figura_clicada = self.ctrl.encontrar_figura_por_id(id_clicado, self.ctrl.modelo_desenho.figuras)
                if figura_clicada:
                    break

        if figura_clicada and figura_clicada in self.ctrl.figuras_selecionadas:
            self.modo_mover = True
            
        elif figura_clicada:
            shift_pressionado = (e.state & 1) != 0
            if not shift_pressionado:
                self.ctrl.figuras_selecionadas.clear()
            
            self.ctrl.figuras_selecionadas.append(figura_clicada)
            self.modo_mover = True
            
        else:
            shift_pressionado = (e.state & 1) != 0
            if not shift_pressionado:
                self.ctrl.figuras_selecionadas.clear()
            
            self.id_caixa = self.ctrl.visao_interface.canvas.create_rectangle(
                self.x_inicio, self.y_inicio, self.x_inicio, self.y_inicio,
                dash=(4, 4), outline="blue", tags="caixa_selecao"
            )

    def atualiza(self, e):
        if self.modo_mover:
            dx = e.x - self.ultimo_x
            dy = e.y - self.ultimo_y
            
            for figura in self.ctrl.figuras_selecionadas:
                # 1. Delega a matemática para o Modelo (Graças ao Composite!)
                figura.mover(dx, dy)
                # 2. Pede para a tela mover os pixels
                self.ctrl.mover_visual(figura, dx, dy)
            
            self.ultimo_x = e.x
            self.ultimo_y = e.y
        else:
            self.ctrl.visao_interface.canvas.coords(
                self.id_caixa, self.x_inicio, self.y_inicio, e.x, e.y
            )

    def finaliza(self, e):
        if self.modo_mover:
            self.modo_mover = False 
        else:
            canvas = self.ctrl.visao_interface.canvas
            x1 = min(self.x_inicio, e.x)
            y1 = min(self.y_inicio, e.y)
            x2 = max(self.x_inicio, e.x)
            y2 = max(self.y_inicio, e.y)

            canvas.delete(self.id_caixa)
            
            if abs(x2 - x1) < 3 and abs(y2 - y1) < 3:
                shift_pressionado = (e.state & 1) != 0
                if not shift_pressionado:
                    self.ctrl.figuras_selecionadas.clear()
                    print("Clicou no vazio. Seleção limpa.")
            else:
                itens_encontrados = canvas.find_overlapping(x1, y1, x2, y2)
                if itens_encontrados:
                    for id_item in itens_encontrados:
                        figura = self.ctrl.encontrar_figura_por_id(id_item, self.ctrl.modelo_desenho.figuras)
                        if figura and figura not in self.ctrl.figuras_selecionadas:
                            self.ctrl.figuras_selecionadas.append(figura)
                            print(f"[+] Selecionou: {figura.__class__.__name__}")
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
        
        self.estado_atual = EstadoForma2Pontos(self, Linha)

    def definir_visao(self, visao):
        self.visao_interface = visao

    def mudar_ferramenta(self, ferramenta):
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
        for figura in self.figuras_selecionadas:
            figura.cor_borda = cor # Funciona para grupos e individuais
            self.pintar_borda_visual(figura, cor)

    def atualizar_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor
        for figura in self.figuras_selecionadas:
            if hasattr(figura, 'cor_preenchimento'):
                figura.cor_preenchimento = cor
            self.pintar_fundo_visual(figura, cor)

    # --- FUNÇÕES AUXILIARES VISUAIS RECURSIVAS (Para suportar Grupos) ---
    def pintar_borda_visual(self, figura, cor):
        if type(figura).__name__ == "FiguraComposta":
            for filho in figura.filhos:
                self.pintar_borda_visual(filho, cor)
        elif hasattr(figura, 'id_tk') and figura.id_tk is not None:
            if type(figura).__name__ in ["Linha", "MaoLivre"]:
                self.visao_interface.canvas.itemconfig(figura.id_tk, fill=cor)
            else:
                self.visao_interface.canvas.itemconfig(figura.id_tk, outline=cor)

    def pintar_fundo_visual(self, figura, cor):
        if type(figura).__name__ == "FiguraComposta":
            for filho in figura.filhos:
                self.pintar_fundo_visual(filho, cor)
        elif hasattr(figura, 'id_tk') and figura.id_tk is not None:
            if type(figura).__name__ not in ["Linha", "MaoLivre"]:
                self.visao_interface.canvas.itemconfig(figura.id_tk, fill=cor)

    def mover_visual(self, figura, dx, dy):
        if type(figura).__name__ == "FiguraComposta":
            for filho in figura.filhos:
                self.mover_visual(filho, dx, dy)
        elif hasattr(figura, 'id_tk') and figura.id_tk is not None:
            self.visao_interface.canvas.move(figura.id_tk, dx, dy)

    def apagar_visual(self, figura):
        if type(figura).__name__ == "FiguraComposta":
            for filho in figura.filhos:
                self.apagar_visual(filho)
        elif hasattr(figura, 'id_tk') and figura.id_tk is not None:
            self.visao_interface.canvas.delete(figura.id_tk)

    def elevar_visual(self, figura):
        if type(figura).__name__ == "FiguraComposta":
            for filho in figura.filhos:
                self.elevar_visual(filho)
        elif hasattr(figura, 'id_tk') and figura.id_tk is not None:
            self.visao_interface.canvas.tag_raise(figura.id_tk)

    def rebaixar_visual(self, figura):
        if type(figura).__name__ == "FiguraComposta":
            for filho in reversed(figura.filhos):
                self.rebaixar_visual(filho)
        elif hasattr(figura, 'id_tk') and figura.id_tk is not None:
            self.visao_interface.canvas.tag_lower(figura.id_tk)

    def encontrar_figura_por_id(self, id_tk, lista_figuras):
        for fig in lista_figuras:
            if type(fig).__name__ == "FiguraComposta":
                encontrada = self.encontrar_figura_por_id(id_tk, fig.filhos)
                if encontrada:
                    return fig # Se achou um filho, retorna o GRUPO inteiro!
            elif hasattr(fig, 'id_tk') and fig.id_tk == id_tk:
                return fig
        return None

    # LÓGICA DO MOUSE 
    def inicia_desenho(self, event): self.estado_atual.inicia(event)
    def atualiza_desenho(self, event): self.estado_atual.atualiza(event)
    def finaliza_desenho(self, event): self.estado_atual.finaliza(event)

    def apagar_selecionados(self, event=None):
        if not self.figuras_selecionadas:
            return
        
        for figura in self.figuras_selecionadas:
            self.apagar_visual(figura) # Função recursiva nova
            if figura in self.modelo_desenho.figuras:
                self.modelo_desenho.figuras.remove(figura)
                
        self.figuras_selecionadas.clear()
        print("Figuras apagadas.")
        
    def encerra_poligono(self, event=None):
        if hasattr(self.estado_atual, 'encerra'):
            self.estado_atual.encerra()

    # FUNÇÕES DA ENTREGA 5 (Copiar/Colar e Camadas)
    def copiar_selecionados(self, event=None):
        self.area_transferencia = []
        for figura in self.figuras_selecionadas:
            self.area_transferencia.append(figura.clonar(offset=15))
        print(f"Copiou {len(self.area_transferencia)} figura(s).")

    def colar_copiados(self, event=None):
        if not hasattr(self, 'area_transferencia') or not self.area_transferencia:
            return
            
        self.figuras_selecionadas.clear()
        for figura in self.area_transferencia:
            self.modelo_desenho.adicionar_figuras(figura)
            self.visao_interface.renderizar_figura(figura, tag="figura_definitiva")
            self.figuras_selecionadas.append(figura)
            
        self.area_transferencia = []
        print("Colado com sucesso!")

    def trazer_para_frente(self, event=None):
        for figura in self.figuras_selecionadas:
            self.modelo_desenho.mover_para_frente(figura)
            self.elevar_visual(figura)

    def enviar_para_tras(self, event=None):
        for figura in self.figuras_selecionadas:
            self.modelo_desenho.mover_para_tras(figura)
            self.rebaixar_visual(figura)

    # --- FUNÇÕES DA ENTREGA 6 (Composite) ---
    def agrupar_selecionadas(self, event=None):
        if len(self.figuras_selecionadas) < 2:
            print("Selecione pelo menos 2 figuras para agrupar.")
            return

        # 1. Cria a caixa (Composite)
        grupo = FiguraComposta(list(self.figuras_selecionadas))

        # 2. Tira os itens soltos do banco principal e coloca o grupo
        for fig in self.figuras_selecionadas:
            if fig in self.modelo_desenho.figuras:
                self.modelo_desenho.figuras.remove(fig)
        self.modelo_desenho.adicionar_figuras(grupo)

        # 3. Atualiza a seleção para ser apenas o grupo
        self.figuras_selecionadas.clear()
        self.figuras_selecionadas.append(grupo)
        print("Figuras agrupadas!")

    def desagrupar_selecionadas(self, event=None):
        novas_selecionadas = []
        houve_desagrupamento = False

        for figura in list(self.figuras_selecionadas):
            if type(figura).__name__ == "FiguraComposta":
                # Tira o grupo do banco principal
                if figura in self.modelo_desenho.figuras:
                    self.modelo_desenho.figuras.remove(figura)
                
                # Devolve os filhos pro banco e seleciona eles
                for filho in figura.filhos:
                    self.modelo_desenho.adicionar_figuras(filho)
                    novas_selecionadas.append(filho)
                    
                houve_desagrupamento = True
            else:
                novas_selecionadas.append(figura)

        if houve_desagrupamento:
            self.figuras_selecionadas = novas_selecionadas
            print("Figuras desagrupadas!")