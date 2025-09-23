<<<<<<< HEAD
=======
# model/distribuicao.py
>>>>>>> 41e954fada5d3360a5540019e9f442d1d1acfa30
import random

class EstiloDistribuicao:
    def rolar_dados(self, quantidade, lados):
        return sum(random.randint(1, lados) for _ in range(quantidade))


class EstiloClassico(EstiloDistribuicao):
    def aplicar(self, personagem=None):
        """Gera e retorna dicionário com valores de atributos (3d6 cada)."""
        atributos = ["forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma"]
        resultado = {}
        for atributo in atributos:
            resultado[atributo] = self.rolar_dados(3, 6)
        return resultado


class EstiloAventureiro(EstiloDistribuicao):
    def gerar_valores(self):
<<<<<<< HEAD
=======
        # 6 valores de 3d6
>>>>>>> 41e954fada5d3360a5540019e9f442d1d1acfa30
        return [self.rolar_dados(3, 6) for _ in range(6)]

    def aplicar(self, personagem=None):
        return {"valores": self.gerar_valores()}


class EstiloHeroico(EstiloDistribuicao):
    def gerar_valores(self):
<<<<<<< HEAD
=======
        # 6 valores: 4d6 drop lowest
>>>>>>> 41e954fada5d3360a5540019e9f442d1d1acfa30
        valores = []
        for _ in range(6):
            dados = [random.randint(1, 6) for _ in range(4)]
            dados.remove(min(dados))
            valores.append(sum(dados))
        return valores

    def aplicar(self, personagem=None):
        return {"valores": self.gerar_valores()}
