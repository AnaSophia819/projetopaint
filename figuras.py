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
    # Definindo o método de contrução de uma figura via contrutor da classe Figura. 
    def desenhar(self, canvas, tags=""):
        # Criação da linha por meio de um método do tkinter. Repare que na crição da linha a cor da borda não importa.
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill= self.cor_borda, tags=tags)