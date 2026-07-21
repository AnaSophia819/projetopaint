import json # Importa a biblioteca nativa do Python para JSON

class Figura:
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

    def clonar(self, offset=15):
        return self.__class__(
            self.x1 + offset, self.y1 + offset, 
            self.x2 + offset, self.y2 + offset, 
            self.cor_borda, self.cor_preenchimento
        )

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

# Função "desenhar" para deixar cada imagem com id próprio
class Linha(Figura):
    def desenhar(self, canvas, tags=""):

        self.id_tk = canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, tags=tags)

class Retangulo(Figura):
    def desenhar(self, canvas, tags=""):

        self.id_tk = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, tags=tags)


class Oval(Figura):
    def desenhar(self, canvas, tags=""):

        self.id_tk = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, tags=tags)


class Poligono(Figura):
    def __init__(self, coordenadas, cor_borda, cor_preenchimento):
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.selecionada = False
        self.id_figura = f"fig_{id(self)}"
        self.id_tk = None

    def desenhar(self, canvas, tags=""):
        self.id_tk = canvas.create_polygon(
            *self.coordenadas, 
            outline=self.cor_borda, fill=self.cor_preenchimento, tags=tags
        )
        return self.id_tk

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

    def clonar(self, offset=15):
        novas_coordenadas = [c + offset for c in self.coordenadas]
        return Poligono(novas_coordenadas, self.cor_borda, self.cor_preenchimento)

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

    def clonar(self, offset=15):
        novas_coordenadas = [c + offset for c in self.coordenadas]
        return MaoLivre(novas_coordenadas, self.cor_borda)

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
        self.figuras = [] 

    def adicionar_figuras(self, figura):
        self.figuras.append(figura)
        
    def limpar(self):
        self.figuras.clear()

    # MÉTODOS DE SALVAR E ABRIR
    def salvar_json(self, caminho_arquivo):
        lista_dicionarios = [fig.para_dicionario() for fig in self.figuras]
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_dicionarios, f, indent=4)

    def abrir_json(self, caminho_arquivo):
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
            nova_figura = criar_figura_de_dicionario(dados)
            self.adicionar_figuras(nova_figura)