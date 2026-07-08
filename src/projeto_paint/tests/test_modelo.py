import unittest
from modelo.figuras import Retangulo, Desenho

class TestModelo(unittest.TestCase):

    def test_criar_figura(self):
        # testae pra ver se guarda as coordenadas
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
        # tester para salvar e abrir
        desenho1 = Desenho()
        desenho1.adicionar_figuras(Retangulo(10, 10, 20, 20, "blue", "blue"))
        
        desenho1.salvar_json("teste_desenho.json")
        
        desenho2 = Desenho()
        desenho2.abrir_json("teste_desenho.json")
        
        # verifica se carregou
        self.assertEqual(len(desenho2.figuras), 1)

if __name__ == '__main__':
    unittest.main()
