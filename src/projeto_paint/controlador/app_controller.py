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
        # Atualiza o ponto enquanto o mouse é arrastado
        self.ctrl.visao_interface.canvas.delete("temporario")
        if self.ctrl.figura_atual:
            self.ctrl.figura_atual.x2, self.ctrl.figura_atual.y2 = e.x, e.y
            # CORREÇÃO MVC: Delega o desenho para a Visão
            self.ctrl.visao_interface.renderizar_figura(self.ctrl.figura_atual, tag="temporario")

    def finaliza(self, e):
        # Salva a figura definitiva ao soltar o botão do mouse 
        if self.ctrl.figura_atual:
            itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
            if itens_temporarios:
                id_gerado = itens_temporarios[-1]
                self.ctrl.figura_atual.id_tk = id_gerado  # Salva o ID do Canvas na figura!
                
                # Altera a tag apenas do item correto
                self.ctrl.visao_interface.canvas.itemconfig(id_gerado, tags="figura_definitiva")
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
        # CORREÇÃO MVC: Delega o desenho para a Visão
        self.ctrl.visao_interface.renderizar_figura(self.ctrl.figura_atual, tag="temporario")

    def finaliza(self, e):
        # Salva o traço definitivo ao soltar o clique
        if self.ctrl.figura_atual:
            itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
            if itens_temporarios:
                id_gerado = itens_temporarios[-1]
                self.ctrl.figura_atual.id_tk = id_gerado  # Salva o ID do Canvas na figura!
                
                self.ctrl.visao_interface.canvas.itemconfig(id_gerado, tags="figura_definitiva")
                self.ctrl.modelo_desenho.adicionar_figuras(self.ctrl.figura_atual)
        self.ctrl.figura_atual = None

class EstadoPoligono(EstadoFerramenta):
    def inicia(self, e):
        # Adiciona coordenadas a cada clique e desenha a partir de 3 pontos 
        self.ctrl.pontos_poligono.extend([e.x, e.y])
        self.ctrl.visao_interface.canvas.delete("temporario")
        if len(self.ctrl.pontos_poligono) >= 6:
            self.ctrl.figura_atual = Poligono(self.ctrl.pontos_poligono, self.ctrl.cor_borda, self.ctrl.cor_preenchimento)
            # CORREÇÃO MVC: Delega o desenho para a Visão
            self.ctrl.visao_interface.renderizar_figura(self.ctrl.figura_atual, tag="temporario")

    def encerra(self):
        # Fecha e salva o polígono ao trocar de ferramenta ou encerrar manualmente
        if self.ctrl.pontos_poligono:
            if self.ctrl.figura_atual:
                itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
                if itens_temporarios:
                    id_gerado = itens_temporarios[-1]
                    self.ctrl.figura_atual.id_tk = id_gerado  # Salva o ID do Canvas na figura!
                    
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

        # Cria uma caixinha invisível de 2 pixels ao redor do clique
        itens_clicados = self.ctrl.visao_interface.canvas.find_overlapping(e.x - 1, e.y - 1, e.x + 1, e.y + 1)
        
        figura_clicada = None
        if itens_clicados:
            # CORREÇÃO: Percorre de trás para frente (prioriza itens visualmente no topo/frente)
            for id_clicado in reversed(itens_clicados):
                for fig in self.ctrl.modelo_desenho.figuras:
                    if hasattr(fig, 'id_tk') and fig.id_tk == id_clicado:
                        figura_clicada = fig
                        break
                if figura_clicada:
                    break

        # 2. Se clicou em uma figura que JÁ ESTÁ na seleção, ativa o movimento
        if figura_clicada and figura_clicada in self.ctrl.figuras_selecionadas:
            self.modo_mover = True
            
        # 3. Se clicou em uma nova figura que NÃO estava selecionada
        elif figura_clicada:
            shift_pressionado = (e.state & 1) != 0
            if not shift_pressionado:
                self.ctrl.figuras_selecionadas.clear()
            
            self.ctrl.figuras_selecionadas.append(figura_clicada)
            self.modo_mover = True  # Começa a mover imediatamente
            
        # 4. Se clicou no vazio, inicia a caixa de seleção azul
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
            # Calcula a distância que o mouse arrastou (delta x, delta y)
            dx = e.x - self.ultimo_x
            dy = e.y - self.ultimo_y
            
            canvas = self.ctrl.visao_interface.canvas
            
            # Move todas as figuras que estão selecionadas
            for figura in self.ctrl.figuras_selecionadas:
                if hasattr(figura, 'id_tk') and figura.id_tk is not None:
                    # Move visualmente no canvas
                    canvas.move(figura.id_tk, dx, dy)
                    
                    # Atualiza as coordenadas internas no Modelo
                    if hasattr(figura, 'x1'):  # Linha, Retângulo, Oval
                        figura.x1 += dx
                        figura.y1 += dy
                        figura.x2 += dx
                        figura.y2 += dy
                    else:
                        # Para Polígono e Mão Livre que usam listas de coordenadas
                        for attr_name in ['pontos', 'coordenadas', 'pontos_poligono', 'coordenadas_atuais']:
                            if hasattr(figura, attr_name):
                                lista = getattr(figura, attr_name)
                                for i in range(0, len(lista), 2):
                                    lista[i] += dx
                                    lista[i+1] += dy
                                break
            
            # Guarda a posição para o próximo cálculo
            self.ultimo_x = e.x
            self.ultimo_y = e.y
        else:
            # Se não está movendo, atualiza o retângulo da caixa de seleção
            self.ctrl.visao_interface.canvas.coords(
                self.id_caixa, self.x_inicio, self.y_inicio, e.x, e.y
            )

    def finaliza(self, e):
        if self.modo_mover:
            self.modo_mover = False  # Soltou o mouse, para de arrastar
        else:
            # Processa as figuras que ficaram dentro da caixa de seleção
            canvas = self.ctrl.visao_interface.canvas
            x1 = min(self.x_inicio, e.x)
            y1 = min(self.y_inicio, e.y)
            x2 = max(self.x_inicio, e.x)
            y2 = max(self.y_inicio, e.y)

            canvas.delete(self.id_caixa)
            
            if abs(x2 - x1) < 3 and abs(y2 - y1) < 3:
                # Foi só um clique simples no vazio, limpa a seleção
                shift_pressionado = (e.state & 1) != 0
                if not shift_pressionado:
                    self.ctrl.figuras_selecionadas.clear()
                    print("Clicou no vazio. Seleção limpa.")
            else:
                # Seleção por arrasto de caixa
                itens_encontrados = canvas.find_overlapping(x1, y1, x2, y2)
                if itens_encontrados:
                    for id_item in itens_encontrados:
                        for figura in self.ctrl.modelo_desenho.figuras:
                            if hasattr(figura, 'id_tk') and figura.id_tk == id_item:
                                if figura not in self.ctrl.figuras_selecionadas:
                                    self.ctrl.figuras_selecionadas.append(figura)
                                    print(f"[+] Selecionou: {figura.__class__.__name__}")
                                break
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
        # ADICIONADO: Se existirem figuras selecionadas, muda a cor da borda delas na hora!
        for figura in self.figuras_selecionadas:
            figura.cor_borda = cor
            if hasattr(figura, 'id_tk') and figura.id_tk is not None:
                if type(figura).__name__ in ["Linha", "MaoLivre"]:
                    self.visao_interface.canvas.itemconfig(figura.id_tk, fill=cor)
                else:
                    self.visao_interface.canvas.itemconfig(figura.id_tk, outline=cor)

    def atualizar_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor
        # ADICIONADO: Se existirem figuras selecionadas, muda a cor do preenchimento delas na hora!
        for figura in self.figuras_selecionadas:
            if hasattr(figura, 'cor_preenchimento'):
                figura.cor_preenchimento = cor
            if hasattr(figura, 'id_tk') and figura.id_tk is not None:
                if type(figura).__name__ not in ["Linha", "MaoLivre"]:
                    self.visao_interface.canvas.itemconfig(figura.id_tk, fill=cor)

    # LÓGICA DO MOUSE 
    
    def inicia_desenho(self, event):
        self.estado_atual.inicia(event)

    def atualiza_desenho(self, event):
        self.estado_atual.atualiza(event)

    def finaliza_desenho(self, event):
        self.estado_atual.finaliza(event)

    def apagar_selecionados(self, event=None):
        if not self.figuras_selecionadas:
            return
        
        canvas = self.visao_interface.canvas
        
        # Percorre a lista de selecionados
        for figura in self.figuras_selecionadas:
            # 1. Apaga visualmente do Canvas
            if hasattr(figura, 'id_tk') and figura.id_tk is not None:
                canvas.delete(figura.id_tk)
            
            # 2. Remove o objeto da memória do Modelo
            if figura in self.modelo_desenho.figuras:
                self.modelo_desenho.figuras.remove(figura)
                
        # 3. Esvazia a nossa lista de seleção
        self.figuras_selecionadas.clear()
        print("Figuras selecionadas foram apagadas com sucesso.")
        
    def encerra_poligono(self, event=None):
        if hasattr(self.estado_atual, 'encerra'):
            self.estado_atual.encerra()

    # FUNÇÕES DA ENTREGA 5 (Copiar/Colar e Camadas)
    
    def copiar_selecionados(self, event=None):
        self.area_transferencia = []
        for figura in self.figuras_selecionadas:
            # Pede para o Modelo criar um clone
            clone = figura.clonar(offset=15)
            self.area_transferencia.append(clone)
        print(f"Copiou {len(self.area_transferencia)} figura(s).")

    def colar_copiados(self, event=None):
        if not hasattr(self, 'area_transferencia') or not self.area_transferencia:
            return
            
        self.figuras_selecionadas.clear()
        
        for figura in self.area_transferencia:
            # 1. Adiciona o clone no banco de dados (Modelo)
            self.modelo_desenho.adicionar_figuras(figura)
            # 2. Desenha o clone na tela (Visão)
            self.visao_interface.renderizar_figura(figura, tag="figura_definitiva")
            # 3. Já deixa o clone selecionado
            self.figuras_selecionadas.append(figura)
            
        # Limpa a área de transferência para forçar um novo CTRL+C antes do próximo CTRL+V
        self.area_transferencia = []
        print("Figuras coladas com sucesso!")

    def trazer_para_frente(self, event=None):
        for figura in self.figuras_selecionadas:
            # Muda a ordem no Modelo
            self.modelo_desenho.mover_para_frente(figura)
            # Muda a ordem visual no Tkinter
            if hasattr(figura, 'id_tk') and figura.id_tk is not None:
                self.visao_interface.canvas.tag_raise(figura.id_tk)

    def enviar_para_tras(self, event=None):
        for figura in self.figuras_selecionadas:
            self.modelo_desenho.mover_para_tras(figura)
            if hasattr(figura, 'id_tk') and figura.id_tk is not None:
                self.visao_interface.canvas.tag_lower(figura.id_tk)