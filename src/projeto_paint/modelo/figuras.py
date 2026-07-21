import json

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
        self.id_tk = None

    def desenhar_caixa_selecao(self, canvas):
        if self.selecionada:
            min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
            min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
            canvas.create_rectangle(
                min_x - 5, min_y - 5, max_x + 5, max_y + 5,
                outline="red", dash=(4, 4), width=2, tags="caixa_selecao"
            )

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

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

class Retangulo(Figura):
    def desenhar(self, canvas, tags=""):
        self.id_tk = canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda, fill=self.cor_preenchimento, tags=tags
        )
        return self.id_tk 

class Linha(Figura):
    def desenhar(self, canvas, tags=""):
        self.id_tk = canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.cor_borda, tags=tags
        )
        return self.id_tk  

class Oval(Figura):
    def desenhar(self, canvas, tags=""):
        self.id_tk = canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda, fill=self.cor_preenchimento, tags=tags
        )
        return self.id_tk  

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
        self.id_tk = None

    def desenhar(self, canvas, tags=""):
        if len(self.coordenadas) >= 4:
            self.id_tk = canvas.create_line(
                *self.coordenadas, fill=self.cor_borda, smooth=True, tags=tags
            )
            return self.id_tk
        return None

    def desenhar_caixa_selecao(self, canvas):
        if self.selecionada and len(self.coordenadas) >= 4:
            xs = self.coordenadas[0::2]
            ys = self.coordenadas[1::2]
            canvas.create_rectangle(
                min(xs) - 5, min(ys) - 5, max(xs) + 5, max(ys) + 5,
                outline="red", dash=(4, 4), width=2, tags="caixa_selecao"
            )

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

class FiguraComposta:
    def __init__(self):
        self.figuras_internas = []
        self.id_tk = None

    def adicionar(self, figura):
        self.figuras_internas.append(figura)
    
    def desenhar(self, canvas, tags=""):
        primeiro_id = None
        for fig in self.figuras_internas:
            id_gerado = fig.desenhar(canvas, tags)
            if primeiro_id is None:
                primeiro_id = id_gerado
        return primeiro_id
    
    def mover(self, dx, dy):
        for fig in self.figuras_internas:
            fig.mover(dx, dy)

    def mudar_cor(self, nova_cor):
        for fig in self.figuras_internas:
            if hasattr(fig, 'cor_borda'):
                fig.cor_borda = nova_cor

class Desenho:
    def __init__(self):
        self.figuras = [] 

    def adicionar_figuras(self, figura):
        self.figuras.append(figura)
        
    def limpar(self):
        self.figuras.clear()

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