import json 
import copy

# Função auxiliar para o JSON conseguir recriar qualquer figura (inclusive as compostas)
def criar_figura_de_dicionario(dados):
    mapa_classes = {
        "Linha": Linha,
        "Retangulo": Retangulo,
        "Oval": Oval,
        "Poligono": Poligono,
        "MaoLivre": MaoLivre,
        "FiguraComposta": FiguraComposta
    }
    ClasseCerta = mapa_classes[dados["tipo"]]
    return ClasseCerta.de_dicionario(dados)

class Figura:
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        self.x1 = x1    
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        
        self.selecionada = False
        self.id_figura = f"fig_{id(self)}"

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


# --- NOVO: PADRÃO COMPOSITE (ENTREGA 6) ---
class FiguraComposta:
    def __init__(self, filhos):
        self.filhos = filhos # Lista que guarda as figuras agrupadas
        self.selecionada = False
        self.id_figura = f"fig_{id(self)}"

    # Quando mandam o grupo mover, ele manda os filhos se moverem
    def mover(self, dx, dy):
        for filho in self.filhos:
            filho.mover(dx, dy)

    # Quando mandam o grupo clonar, ele clona todos os filhos
    def clonar(self, offset=15):
        novos_filhos = [filho.clonar(offset) for filho in self.filhos]
        return FiguraComposta(novos_filhos)

    # Propriedades "Mágicas": Se o Controlador tentar mudar a cor do grupo,
    # essa propriedade intercepta e muda a cor de todos os filhos lá dentro.
    @property
    def cor_borda(self):
        return self.filhos[0].cor_borda if self.filhos else ""

    @cor_borda.setter
    def cor_borda(self, cor):
        for filho in self.filhos:
            filho.cor_borda = cor

    @property
    def cor_preenchimento(self):
        return self.filhos[0].cor_preenchimento if self.filhos and hasattr(self.filhos[0], 'cor_preenchimento') else ""

    @cor_preenchimento.setter
    def cor_preenchimento(self, cor):
        for filho in self.filhos:
            if hasattr(filho, 'cor_preenchimento'):
                filho.cor_preenchimento = cor

    def para_dicionario(self):
        return {
            "tipo": "FiguraComposta",
            "filhos": [filho.para_dicionario() for filho in self.filhos]
        }

    @classmethod
    def de_dicionario(cls, dados):
        filhos_instanciados = [criar_figura_de_dicionario(d) for d in dados["filhos"]]
        return cls(filhos_instanciados)


# --- GERENCIADOR DO ARQUIVO ---
class Desenho:
    def __init__(self):
        self.figuras = [] 

    def adicionar_figuras(self, figura):
        self.figuras.append(figura)
        
    def limpar(self):
        self.figuras.clear()

    def mover_para_frente(self, figura):
        if figura in self.figuras:
            self.figuras.remove(figura)
            self.figuras.append(figura) 

    def mover_para_tras(self, figura):
        if figura in self.figuras:
            self.figuras.remove(figura)
            self.figuras.insert(0, figura) 

    def salvar_json(self, caminho_arquivo):
        lista_dicionarios = [fig.para_dicionario() for fig in self.figuras]
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_dicionarios, f, indent=4)

    def abrir_json(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            lista_dicionarios = json.load(f)
        
        self.limpar() 
        for dados in lista_dicionarios:
            nova_figura = criar_figura_de_dicionario(dados)
            self.adicionar_figuras(nova_figura)