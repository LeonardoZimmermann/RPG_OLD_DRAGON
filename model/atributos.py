<<<<<<< HEAD
=======
# model/atributos.py

>>>>>>> 41e954fada5d3360a5540019e9f442d1d1acfa30
class Atributos:
    def __init__(self):
        self.forca = 0
        self.destreza = 0
        self.constituicao = 0
        self.inteligencia = 0
        self.sabedoria = 0
        self.carisma = 0

    def to_dict(self):
        return {
            "forca": self.forca,
            "destreza": self.destreza,
            "constituicao": self.constituicao,
            "inteligencia": self.inteligencia,
            "sabedoria": self.sabedoria,
            "carisma": self.carisma
        }

    def exibir_atributos(self):
        for k, v in self.to_dict().items():
            print(f"{k.capitalize()}: {v}")


class Personagem:
    def __init__(self, nome):
        self.nome = nome
        self.atributos = Atributos()
        self.classe = None
        self.raca = None

    def exibir_personagem(self):
        print("==============================")
        print(f"Nome: {self.nome}")
        self.atributos.exibir_atributos()
        if self.raca:
            self.raca.exibir_info()
        if self.classe:
            self.classe.exibir_info()
        print("==============================")
