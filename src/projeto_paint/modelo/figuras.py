import json # Importa a biblioteca nativa do Python para JSON
import copy

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

    # Mover para Linha, Retangulo e Oval 
    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    # CLONAR (Para o CTRL-C / CTRL-V)
    def clonar(self, offset=15):
        # self.__class__ garante que ele vai criar a classe certa (Linha, Retangulo ou Oval)
        return self.__class__(
            self.x1 + offset, self.y1 + offset, 
            self.x2 + offset, self.y2 + offset, 
            self.cor_borda, self.cor_preenchimento
        )

    def para_dicionario(self):
        return {
            "tipo": self.__class__.__name__, 
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

    # Mover para o Poligono 
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

    # Mover para a MaoLivre 
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


# GERENCIADOR DO ARQUIVO
class Desenho:
    def __init__(self):
        self.figuras = [] # Vai guardar os objetos 

    def adicionar_figuras(self, figura):
        self.figuras.append(figura)
        
    def limpar(self):
        self.figuras.clear()

    # MÉTODOS DE ORDEM DE CAMADAS
    def mover_para_frente(self, figura):
        if figura in self.figuras:
            self.figuras.remove(figura)
            self.figuras.append(figura) # Coloca no final da lista (desenha por último = fica na frente)

    def mover_para_tras(self, figura):
        if figura in self.figuras:
            self.figuras.remove(figura)
            self.figuras.insert(0, figura) # Coloca no índice 0 (desenha primeiro = fica atrás)

    # MÉTODOS DE SALVAR E ABRIR
    def salvar_json(self, caminho_arquivo):
        lista_dicionarios = [fig.para_dicionario() for fig in self.figuras]
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_dicionarios, f, indent=4)

    def abrir_json(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            lista_dicionarios = json.load(f)
        
        self.limpar() 
        
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