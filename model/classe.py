# model/classe.py

class ClassePersonagem:
    def __init__(self, nome, vida, armas, armaduras, itens_magicos, habilidades):
        self.nome = nome
        self.vida = vida
        self.armas = armas
        self.armaduras = armaduras
        self.itens_magicos = itens_magicos
        self.habilidades = habilidades[:]

    def exibir_info(self):
        print(f"\n-- Classe: {self.nome} --")
        print(f"Vida: {self.vida}")
        print(f"Armas: {self.armas}")
        print(f"Armaduras: {self.armaduras}")
        print(f"Itens mágicos: {self.itens_magicos}")
        print(f"Habilidades: {self.habilidades}")


class Guerreiro(ClassePersonagem):
    def __init__(self):
        super().__init__(
            nome="Guerreiro",
            vida=10,
            armas="Pode usar todas as armas.",
            armaduras="Pode usar todas as armaduras.",
            itens_magicos="Não pode usar cajados, varinhas e pergaminhos, exceto pergaminho de proteção.",
            habilidades=["Ataque Extra", "Especialista em Combate"]
        )


class Ladrao(ClassePersonagem):
    def __init__(self):
        super().__init__(
            nome="Ladrão",
            vida=6,
            armas="Apenas armas pequenas ou médias.",
            armaduras="Apenas armaduras leves.",
            itens_magicos="Não pode usar cajados, varinhas e pergaminhos, exceto pergaminhos de proteção.",
            habilidades=["Ataque Furtivo", "Ouvir Ruídos", "Arrombar"]
        )


class Mago(ClassePersonagem):
    def __init__(self):
        super().__init__(
            nome="Mago",
            vida=4,
            armas="Apenas armas pequenas.",
            armaduras="Nenhuma; armaduras impedem conjuração.",
            itens_magicos="Pode usar todos os tipos de itens mágicos.",
            habilidades=["Ler Magias", "Detectar Magias", "Conjurar Magias"]
        )
