from flask import Flask, render_template, request
from model import (
    Personagem, EstiloClassico, EstiloAventureiro, EstiloHeroico,
    Humano, Elfo, Anao, Halfling, Guerreiro, Ladrao, Mago
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome", "SemNome")
        estilo = request.form.get("estilo")
        raca = request.form.get("raca")
        classe = request.form.get("classe")

        personagem = Personagem(nome)

        if estilo == "classico":
            vals = EstiloClassico().aplicar()
            for k, v in vals.items():
                setattr(personagem.atributos, k, v)
            personagem.raca = {"humano": Humano, "elfo": Elfo, "anao": Anao, "halfling": Halfling}[raca]()
            personagem.classe = {"guerreiro": Guerreiro, "ladrao": Ladrao, "mago": Mago}[classe]()
            return render_template("summary.html", personagem=personagem)

        if estilo == "aventureiro":
            valores = EstiloAventureiro().gerar_valores()
        elif estilo == "heroico":
            valores = EstiloHeroico().gerar_valores()
        else:
            return "Estilo inválido", 400

        return render_template(
            "assign.html",
            nome=nome,
            estilo=estilo,
            raca=raca,
            classe=classe,
            valores=list(enumerate(valores))
        )

    # GET
    racas = [("humano", "Humano"), ("elfo", "Elfo"), ("anao", "Anão"), ("halfling", "Halfling")]
    classes = [("guerreiro", "Guerreiro"), ("ladrao", "Ladrão"), ("mago", "Mago")]
    return render_template("index.html", racas=racas, classes=classes)


@app.route("/create", methods=["POST"])
def create():
    nome = request.form.get("nome", "SemNome")
    estilo = request.form.get("estilo")
    raca_key = request.form.get("raca")
    classe_key = request.form.get("classe")

    atributos_keys = ["forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma"]
    personagem = Personagem(nome)

    for chave in atributos_keys:
        sel = request.form.get(chave)
        if not sel:
            return "Por favor atribua todos os valores aos atributos.", 400
        try:
            valor_str, idx = sel.split("|")
            valor = int(valor_str)
        except Exception:
            return "Formato de valor inválido.", 400
        setattr(personagem.atributos, chave, valor)

    raca_map = {"humano": Humano, "elfo": Elfo, "anao": Anao, "halfling": Halfling}
    classe_map = {"guerreiro": Guerreiro, "ladrao": Ladrao, "mago": Mago}
    personagem.raca = raca_map.get(raca_key, Humano)()
    personagem.classe = classe_map.get(classe_key, Guerreiro)()

    return render_template("summary.html", personagem=personagem)


if __name__ == "__main__":
    app.run(debug=True)
