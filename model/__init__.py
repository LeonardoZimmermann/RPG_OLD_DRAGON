# model/__init__.py
from .atributos import Personagem, Atributos
from .classe import ClassePersonagem, Guerreiro, Ladrao, Mago
from .raca import Raca, Humano, Elfo, Anao, Halfling
from .distribuicao import EstiloClassico, EstiloAventureiro, EstiloHeroico

__all__ = [
    "Personagem", "Atributos",
    "ClassePersonagem", "Guerreiro", "Ladrao", "Mago",
    "Raca", "Humano", "Elfo", "Anao", "Halfling",
    "EstiloClassico", "EstiloAventureiro", "EstiloHeroico"
]
