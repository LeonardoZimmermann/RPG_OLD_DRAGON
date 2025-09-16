# model/raca.py

class Raca:
    def __init__(self, nome, movimento, infravisao, alinhamento, habilidade_especial):
        self.nome = nome
        self.movimento = movimento
        self.infravisao = infravisao
        self.alinhamento = alinhamento
        self.habilidade_especial = habilidade_especial

    def exibir_info(self):
        print(f"\n-- Raça: {self.nome} --")
        print(f"Movimento: {self.movimento}")
        print(f"Infravisão: {self.infravisao}")
        print(f"Alinhamento: {self.alinhamento}")
        print(f"Habilidade especial: {self.habilidade_especial}")


class Humano(Raca):
    def __init__(self):
        super().__init__("Humano", "9m", "Nenhum", "Qualquer", "Versatilidade")


class Elfo(Raca):
    def __init__(self):
        super().__init__("Elfo", "9m", "18m", "Caótico/Bom", "Visão aguçada")


class Anao(Raca):
    def __init__(self):
        super().__init__("Anão", "6m", "18m", "Leal/Neutro", "Resistência")


class Halfling(Raca):
    def __init__(self):
        super().__init__("Halfling", "7,5m", "Nenhum", "Neutro", "Agilidade")
