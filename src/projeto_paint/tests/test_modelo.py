import unittest
import os
from modelo.figuras import Retangulo, Desenho

class TestModeloPaint(unittest.TestCase):

    def test_geometria_e_serializacao(self):
        # Testa a criação e o round-trip (Figura -> Dicionário -> Figura) de uma vez só
        ret = Retangulo(10, 10, 50, 50, "black", "blue")
        self.assertEqual(ret.x1, 10) # Garante que guardou a coordenada
        
        dicionario = ret.para_dicionario()
        ret_novo = Retangulo.de_dicionario(dicionario)
        
        self.assertEqual(ret_novo.cor_preenchimento, "blue")
        self.assertIsInstance(ret_novo, Retangulo)

    def test_ciclo_salvar_abrir(self):
        # Testa criar um desenho, salvar no HD e abrir de novo
        desenho = Desenho()
        desenho.adicionar_figuras(Retangulo(0, 0, 10, 10, "red", ""))
        
        caminho = "teste.json"
        desenho.salvar_json(caminho)
        
        novo_desenho = Desenho()
        novo_desenho.abrir_json(caminho)
        
        self.assertEqual(len(novo_desenho.figuras), 1)
        self.assertIsInstance(novo_desenho.figuras[0], Retangulo)
        
        # Limpa o arquivo de teste no final
        if os.path.exists(caminho):
            os.remove(caminho)

if __name__ == '__main__':
    unittest.main()
