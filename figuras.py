import tkinter as tk
from tkinter import colorchooser

# Criação da classe figura que será o molde de cada figura disponível para desenhar.
class Figura:
    # Aqui é o método especial contrutor que será inicializado automaticamente na criação de qualquer figura e nele temos 7 parâmetros, sendo o primeiro obrigatório para qualquer chamada de método, do segundo ao quinto coordenadas da figura, o sexto a cor da borda e o 7 a cor do preenchimento
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
    # Criação do metódo mais importante do programa, o método responsável por fazer o desenho na tela. Para isso, é preciso 2 parâmetros além do "self" o "canvas" e "tags". Para desenhar é necessário uma tela, essa tela é justamente o canvas, sempre que esse método for chamado por alguma subclasse figura, vamos precisar de uma referência de onde desenhar, aí que o canvas entra como argumento. Já o parâmetro tags é o responsável por orientar o estado em que a figura está, se está em andamento ou finalizada, quando usada como argumento por alguma subclasse vai se comportar como uma variável indicando o estado da figura.
    def desenhar(self, canvas, tags=""):
        raise NotADirectoryError()
    
# Criação da classe Linha. A classe Linha recebe como argumento "Figura" porque ela é uma subclasse de figura.
class Linha(Figura):
    # Definindo o método de contrução de uma figura via classe Figura. 
    def desenhar(self, canvas, tags=""):
        # Criação da linha por meio de um método do tkinter. Repare que na crição da linha a cor do preenchimento não importa.
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, tags=tags)
    
# Criação da classe Retangulo. E como é subclasse de Figura recebe como argumento Figura.
class Retangulo(Figura):
   # Definindo o método de contrução de uma figura via classe Figura.
   def desenhar(self, canvas, tags=""):
       # Criação do retângulo por meio de um método nativo do tkinter.
       return canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, tags=tags)

# Criação da classe Oval.
class Oval(Figura):
    # Implementação do método desenhar da classe Figura.
    def desenhar(self, canvas, tags=""):
        # Criação do oval por meio de um método nativo do tkinter
        return canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, tags=tags)
    
# Criação da classe polígono.
class Poligono(Figura):
    # Diferente das figuras o polígono precisa de vários pontos para ser criado. Como o contrutor é limitado a apenas 4 coordenadas, vamos precisar criar um crontutor exclusivo para essa figura. Nesse novo construtor ao invés de colocarmos pontos em variáveis únicas, vamos colocá-los em uma lista.
    def __init__(self, coordenadas, cor_borda, cor_preenchimento):
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    # Implementação do método desenhar da classe Figura.
    def desenhar(self, canvas, tags=""):
        # Criação do polígono por meio de um método nativo do tkinter
        return canvas.create_polygon(self.coordenadas, outline=self.cor_borda, fill=self.cor_preenchimento, tags=tags)
    
    # Criação da classe MaoLivre.
class MaoLivre(Figura):
    # Sobrescrevendo o construtor, pois também precisamos de uma lista de coordenadas. E como não tem preenchimento,  não vamos colocar como parâmetro.
    def __init__(self, coordenadas, cor_borda):
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda

    # Definindo o método de desenho por meio da classe Figura.
    def desenhar(self, canvas, tags=""):
        # Um desenho qualque tipo um rabisco é meio que uma fusão entre linhas e polígonos. São linhas que começam e terminam no mesmo ponto ao decorrer do movimento do mouse. E também não precisa de cor de preenchimento.
        return canvas.create_line(self.coordenadas, fill=self.cor_borda, tags=tags)


