# tirei o tkinter (regra MVC: aqui fica apenas a estrutura de dados. Sem import tkinter)

# Criação da classe figura que será o molde de cada figura disponível para desenhar.
class Figura:
    # Aqui é o método especial construtor que será inicializado automaticamente na criação de qualquer figura e nele temos 7 parâmetros, sendo o primeiro obrigatório para qualquer chamada de método, do segundo ao quinto coordenadas da figura, o sexto a cor da borda e o 7 a cor do preenchimento
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        self.x1 = x1    
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
    
class Linha(Figura):
    pass

class Retangulo(Figura):
    pass

class Oval(Figura):
    pass


# Classe que o professor pediu para armazenar a lista de desenhos feitos
class Desenho:
    def __init__(self):
        self.figuras = [] # Vai guardas os objetos (Linha, Retangulo ...)

    def adicionar_figuras(self, figura):
        self.figuras.append(figura)
        
    def limpar(self):
        self.figuras.clear()

