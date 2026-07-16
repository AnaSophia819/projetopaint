import json # Importa a biblioteca nativa do Python para JSON

class Figura:
    # Aqui é  para   iniciar automaticamente
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        self.x1 = x1    
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        
        self.selecionada = False
        self.id_figura = f"fig_{id(self)}" # Cria o crachá único da figura

    def desenhar_caixa_selecao(self, canvas):
        if self.selecionada:
            min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
            min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
            canvas.create_rectangle(
                min_x - 5, min_y - 5, max_x + 5, max_y + 5,
                outline="red", dash=(4, 4), width=2, tags="caixa_selecao"
            )

    #  Mover para Linha, Retangulo e Oval 
    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def para_dicionario(self):
        return {
            "tipo": self.__class__.__name__, # Salva se é Linha, Retangulo ou Oval
            "x1": self.x1, "y1": self.y1,
            "x2": self.x2, "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            dados["x1"], dados["y1"], 
            dados["x2"], dados["y2"], 
            dados["cor_borda"], dados["cor_preenchimento"]
        )

class Linha(Figura):
    pass

class Retangulo(Figura):
    pass

class Oval(Figura):
    pass

class Poligono(Figura):
    def __init__(self, coordenadas, cor_borda, cor_preenchimento):
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        
        self.selecionada = False
        self.id_figura = f"fig_{id(self)}"

    def desenhar_caixa_selecao(self, canvas):
        if self.selecionada and len(self.coordenadas) >= 4:
            xs = self.coordenadas[0::2]
            ys = self.coordenadas[1::2]
            canvas.create_rectangle(
                min(xs) - 5, min(ys) - 5, max(xs) + 5, max(ys) + 5,
                outline="red", dash=(4, 4), width=2, tags="caixa_selecao"
            )

    #  Mover para o Poligono 
    def mover(self, dx, dy):
        for i in range(0, len(self.coordenadas), 2):
            self.coordenadas[i] += dx      
            self.coordenadas[i+1] += dy     

    def para_dicionario(self):
        return {
            "tipo": "Poligono",
            "coordenadas": self.coordenadas,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(dados["coordenadas"], dados["cor_borda"], dados["cor_preenchimento"])

class MaoLivre(Figura):
    def __init__(self, coordenadas, cor_borda):
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = ""
        
        self.selecionada = False
        self.id_figura = f"fig_{id(self)}"
 
    def desenhar_caixa_selecao(self, canvas):
        if self.selecionada and len(self.coordenadas) >= 4:
            xs = self.coordenadas[0::2]
            ys = self.coordenadas[1::2]
            canvas.create_rectangle(
                min(xs) - 5, min(ys) - 5, max(xs) + 5, max(ys) + 5,
                outline="red", dash=(4, 4), width=2, tags="caixa_selecao"
            )

    #  Mover para a MaoLivre 
    def mover(self, dx, dy):
        for i in range(0, len(self.coordenadas), 2):
            self.coordenadas[i] += dx       
            self.coordenadas[i+1] += dy    

    def para_dicionario(self):
        return {
            "tipo": "MaoLivre",
            "coordenadas": self.coordenadas,
            "cor_borda": self.cor_borda
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(dados["coordenadas"], dados["cor_borda"])


#  GERENCIADOR DO ARQUIVO

class Desenho:
    def __init__(self):
        self.figuras = [] # Vai guardar os objetos 

    def adicionar_figuras(self, figura):
        self.figuras.append(figura)
        
    def limpar(self):
        self.figuras.clear()

    # MÉTODOS DE SALVAR E ABRIR
    def salvar_json(self, caminho_arquivo):
        # Transforma todas as figuras da lista em dicionários
        lista_dicionarios = [fig.para_dicionario() for fig in self.figuras]
        
        # coloca o arquivo no disco
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_dicionarios, f, indent=4)

    def abrir_json(self, caminho_arquivo):
        # Lê o arquivo do disco
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            lista_dicionarios = json.load(f)
        
        self.limpar() 
        
        # Dicionário para descobrir qual classe instanciar a partir  do JSON
        mapa_classes = {
            "Linha": Linha,
            "Retangulo": Retangulo,
            "Oval": Oval,
            "Poligono": Poligono,
            "MaoLivre": MaoLivre
        }
        
        for dados in lista_dicionarios:
            tipo_figura = dados["tipo"]
            ClasseCerta = mapa_classes[tipo_figura]
            nova_figura = ClasseCerta.de_dicionario(dados)
            self.adicionar_figuras(nova_figura)
