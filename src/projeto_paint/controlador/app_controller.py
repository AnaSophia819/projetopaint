from modelo.figuras import Desenho, Linha, Retangulo, Oval, Poligono, MaoLivre
from abc import ABC, abstractmethod

# Criando a classe base para todos os comandos

class Comando(ABC):
    @abstractmethod
    def executar(self):
        pass

    @abstractmethod
    def desfazer(self):
        pass

# Comando para adicionar figuras
class Adicionar(Comando):
    def __init__(self, modelo_desenho, figura, controlador):
        self.modelo = modelo_desenho
        self.figura = figura
        self.controlador = controlador

    def executar(self):
        self.modelo.adicionar_figuras(self.figura)
        self.controlador.redesenhar_canvas()

    def desfazer(self):
        if self.figura in self.modelo.figuras:
            self.modelo.figuras.remove(self.figura)
        self.controlador.redesenhar_canvas()

# Comando para apagar figuras
class Apagar(Comando):
    def __init__(self, modelo_desenho, figuras_apagar, controlador):
        self.modelo = modelo_desenho
        self.figuras_apagar = list(figuras_apagar)
        self.controlador = controlador

    def executar(self):
        for fig in self.figuras_apagar:
           if fig in self.modelo.figuras:
                self.modelo.figuras.remove(fig)
        self.controlador.redesenhar_canvas()

    def desfazer(self):
        for fig in self.figuras_apagar:
            self.modelo.adicionar_figuras(fig)
        self.controlador.redesenhar_canvas()

# Comando para mover figuras
class Mover(Comando):

    def __init__(self, figuras, dx, dy, controlador):
        self.figuras = list(figuras)
        self.dx = dx
        self.dy = dy
        self.controlador = controlador

    def executar(self):
        for fig in self.figuras:
            fig.mover(self.dx, self.dy)
        self.controlador.redesenhar_canvas()

    def desfazer(self):
        # Para desfazer a movimentação, movemos no sentido inverso (-dx, -dy)
        for fig in self.figuras:
            fig.mover(-self.dx, -self.dy)
        self.controlador.redesenhar_canvas()

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
            self.ctrl.figura_atual.desenhar(self.ctrl.visao_interface.canvas, tags="temporario")

    def finaliza(self, e):
        # Salva a figura definitiva ao soltar o botão do mouse 
        if self.ctrl.figura_atual:
            # CORREÇÃO: Busca o ID gerado pelo Tkinter usando a tag temporária antes de renomeá-la
            itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
            if itens_temporarios:
                id_gerado = itens_temporarios[-1]
                self.ctrl.figura_atual.id_tk = id_gerado  # Salva o ID do Canvas na figura!
                
                # Altera a tag apenas do item correto
                self.ctrl.visao_interface.canvas.itemconfig(id_gerado, tags="figura_definitiva")
                
                # 1. Guarda a referência da figura criada
                fig_para_adicionar = self.ctrl.figura_atual
                self.ctrl.figura_atual = None
                
                # 2. Cria o comando passando a figura
                cmd = Adicionar(self.ctrl.modelo_desenho, fig_para_adicionar, self.ctrl)
                self.ctrl.executar_comando(cmd)

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
        if self.ctrl.figura_atual:
            itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
            if itens_temporarios:
                id_gerado = itens_temporarios[-1]
                self.ctrl.figura_atual.id_tk = id_gerado  # Salva o ID do Canvas na figura!
                
                self.ctrl.visao_interface.canvas.itemconfig(id_gerado, tags="figura_definitiva")
                fig_para_adicionar = self.ctrl.figura_atual
                self.ctrl.figura_atual = None
                
                cmd = Adicionar(self.ctrl.modelo_desenho, fig_para_adicionar, self.ctrl)
                self.ctrl.executar_comando(cmd)

class EstadoPoligono(EstadoFerramenta):
    def inicia(self, e):
        # Adiciona coordenadas a cada clique e desenha a partir de 3 pontos 
        self.ctrl.pontos_poligono.extend([e.x, e.y])
        self.ctrl.visao_interface.canvas.delete("temporario")
        if len(self.ctrl.pontos_poligono) >= 6:
            self.ctrl.figura_atual = Poligono(self.ctrl.pontos_poligono, self.ctrl.cor_borda, self.ctrl.cor_preenchimento)
            self.ctrl.figura_atual.desenhar(self.ctrl.visao_interface.canvas, tags="temporario")

    def encerra(self):
        if self.ctrl.pontos_poligono:
            if self.ctrl.figura_atual:
                itens_temporarios = self.ctrl.visao_interface.canvas.find_withtag("temporario")
                if itens_temporarios:
                    id_gerado = itens_temporarios[-1]
                    self.ctrl.figura_atual.id_tk = id_gerado
                    self.ctrl.visao_interface.canvas.itemconfig(id_gerado, tags="figura_definitiva")
                    
                    # Gera o comando para o polígono
                    fig_para_adicionar = self.ctrl.figura_atual
                    cmd = Adicionar(self.ctrl.modelo_desenho, fig_para_adicionar, self.ctrl)
                    self.ctrl.executar_comando(cmd)

            self.ctrl.pontos_poligono = []
            self.ctrl.figura_atual = None

class EstadoSelecionar(EstadoFerramenta):
    def __init__(self, ctrl):
        super().__init__(ctrl)
        self.id_caixa = None
    def inicia(self, e):
        self.modo_mover = False
        self.x_inicio = e.x
        self.y_inicio = e.y
        self.ultimo_x = e.x
        self.ultimo_y = e.y
        self.dx_total = 0
        self.dy_total = 0

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
        
        self.ctrl.redesenhar_canvas()

    def atualiza(self, e):
        if self.modo_mover:
            # Calcula a distância que o mouse arrastou (delta x, delta y)
            dx = e.x - self.ultimo_x
            dy = e.y - self.ultimo_y
            
            # Acumula o movimento total
            self.dx_total += dx
            self.dy_total += dy
            
            canvas = self.ctrl.visao_interface.canvas
            
            # Move todas as figuras que estão selecionadas
            for figura in self.ctrl.figuras_selecionadas:
                if hasattr(figura, 'id_tk') and figura.id_tk is not None:
                    # Move visualmente no canvas
                    canvas.move(figura.id_tk, dx, dy)
            
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

            # Soltou o mouse: dispara O COMANDO de mover com o deslocamento TOTAL
            if self.dx_total != 0 or self.dy_total != 0:
                cmd = Mover(self.ctrl.figuras_selecionadas, self.dx_total, self.dy_total, self.ctrl)
                self.ctrl.executar_comando(cmd)

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

            self.ctrl.redesenhar_canvas()

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
        self.pilha_undo = []
        self.pilha_redo = []
        
        # Define o estado inicial
        self.estado_atual = EstadoForma2Pontos(self, Linha)

    def executar_comando(self, comando):
        comando.executar()
        self.pilha_undo.append(comando)
        self.pilha_redo.clear()

    def undo(self, event=None):
        if self.pilha_undo:
            cmd = self.pilha_undo.pop()
            cmd.desfazer()
            self.pilha_redo.append(cmd)

    def redo(self, event=None):
        if self.pilha_redo:
            cmd = self.pilha_redo.pop()
            cmd.executar()
            self.pilha_undo.append(cmd)

    def redesenhar_canvas(self):
        if not self.visao_interface:  
            return
        
        canvas = self.visao_interface.canvas
        canvas.delete("all")
        
        for fig in self.modelo_desenho.figuras:
            fig.id_tk = fig.desenhar(canvas, tags="figura_definitiva")
        
            if hasattr(fig, 'desenhar_caixa_selecao') and fig in self.figuras_selecionadas:
                fig.desenhar_caixa_selecao(canvas)

    def definir_visao(self, visao):
        self.visao_interface = visao

    def mudar_ferramenta(self, ferramenta):
        # Fecha polígonos abertos antes de trocar de ferramenta
        if hasattr(self.estado_atual, 'encerra'):
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

        if self.visao_interface and hasattr(self.visao_interface, 'cb_ferramenta'):
            self.visao_interface.cb_ferramenta.set(ferramenta)

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

    def apagar_selecionados(self, event=None):
        if not self.figuras_selecionadas:
            return
    
        # Executa a deleção através do Padrão Command
        cmd = Apagar(self.modelo_desenho, self.figuras_selecionadas, self)
        self.executar_comando(cmd)
        
        # Limpa a seleção atual
        self.figuras_selecionadas.clear()
        
    def encerra_poligono(self, event=None):
        if hasattr(self.estado_atual, 'encerra'):
            self.estado_atual.encerra()