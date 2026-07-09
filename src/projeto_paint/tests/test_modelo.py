import unittest
import os
import sys

# Esse bloco garante que o teste ache o arquivo 'figuras.py' na raiz,
# mesmo estando dentro da pasta 'tests' lá no Git
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from figuras import Retangulo, Desenho  # Correção do 'Desenho' aqui!

class TestModelo(unittest.TestCase):

    def test_criar_figura(self):
        # testa para ver se guarda as coordenadas
        ret = Retangulo(10, 20, 100, 200, "black", "blue")
        self.assertEqual(ret.x1, 10)
        self.assertEqual(ret.y2, 200)

    def test_dicionario(self):
        # testando o round-trip
        ret = Retangulo(0, 0, 50, 50, "red", "")
        dic = ret.para_dicionario()
        
        self.assertEqual(dic["tipo"], "Retangulo")
        
        novo_ret = Retangulo.de_dicionario(dic)
        self.assertEqual(novo_ret.cor_borda, "red")
        self.assertEqual(novo_ret.x2, 50)

    def test_json(self):
        # teste para salvar e abrir
        desenho1 = Desenho()
        desenho1.adicionar_figuras(Retangulo(10, 10, 20, 20, "blue", "blue"))
        
        nome_arquivo = "teste_desenho.json"
        desenho1.salvar_json(nome_arquivo)
        
        desenho2 = Desenho()
        desenho2.abrir_json(nome_arquivo)
        
        # verifica se carregou
        self.assertEqual(len(desenho2.figuras), 1)
        
        # limpa o arquivo temporário
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)

if __name__ == '__main__':
    unittest.main(verbosity=2)
