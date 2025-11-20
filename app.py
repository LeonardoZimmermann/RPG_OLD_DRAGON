import os
import json
from flask import Flask, render_template, request, redirect, url_for

# imports do seu pacote model (ajuste nomes se for diferente)
from model.atributos import Atributos
from model.classe import Guerreiro, Ladrao, Mago
from model.raca import Humano, Elfo, Anao, Halfling
from model.distribuicao import EstiloClassico, EstiloAventureiro, EstiloHeroico

app = Flask(__name__)

# Mapeamentos para criar classes/raças a partir do form
CLASSES = {
    "guerreiro": Guerreiro,
    "ladrao": Ladrao,
    "mago": Mago
}

RACAS = {
    "humano": Humano,
    "elfo": Elfo,
    "anao": Anao,
    "halfling": Halfling
}

ESTILOS = {
    "classico": EstiloClassico,
    "aventureiro": EstiloAventureiro,
    "heroico": EstiloHeroico
}


def save_personagem_json(personagem, folder="saves"):
    """
    Salva personagem em JSON. Recebe objeto (Atributos) e converte com __dict__.
    Converte classe e raca para dicts com campos relevantes.
    Retorna caminho do arquivo salvo.
    """
    os.makedirs(folder, exist_ok=True)

    nome = getattr(personagem, "nome", "personagem").strip() or "personagem"
    safe_name = "".join(c for c in nome if c.isalnum() or c in (" ", "-", "_")).rstrip()
    filename = os.path.join(folder, f"{safe_name}.json")

    # Base: cópia do __dict__
    data = {}
    for k, v in getattr(personagem, "__dict__", {}).items():
        if k.startswith("_"):
            continue
        # evitamos atributos que são métodos/funcs
        if callable(v):
            continue
        data[k] = v

    # converte classe/raça para dicionários legíveis
    if "classe" in data and data["classe"] is not None:
        cls = data["classe"]
        data["classe"] = {
            "nome": getattr(cls, "nome", str(cls)),
            "vida": getattr(cls, "vida", None),
            "armas": getattr(cls, "armas", None),
            "armaduras": getattr(cls, "armaduras", None),
            "itens_magicos": getattr(cls, "itens_magicos", None),
            "habilidades": getattr(cls, "habilidades", None),
        }

    if "raca" in data and data["raca"] is not None:
        rc = data["raca"]
        data["raca"] = {
            "nome": getattr(rc, "nome", str(rc)),
            "movimento": getattr(rc, "movimento", None),
            "infravisao": getattr(rc, "infravisao", None),
            "alinhamento": getattr(rc, "alinhamento", None),
            "habilidade_especial": getattr(rc, "habilidade_especial", None),
        }

    # transforma objetos complexos em strings recursivamente (safeguard)
    def make_json_serializable(obj):
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        if isinstance(obj, (list, tuple)):
            return [make_json_serializable(x) for x in obj]
        if isinstance(obj, dict):
            return {k: make_json_serializable(v) for k, v in obj.items()}
        return str(obj)

    data = make_json_serializable(data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filename


def try_generate_values_from_style(estilo_key):
    """
    Tenta obter uma lista de 6 valores de atributo a partir da classe de estilo.
    Suporta distribuições que implementam:
      - gerar_valores() -> list
      - gerar() -> list
      - aplicar(personagem) -> modifica um objeto Atributos (criamos temporário)
    Retorna lista de 6 inteiros.
    """
    EstiloCls = ESTILOS.get(estilo_key)
    if EstiloCls is None:
        raise ValueError("Estilo desconhecido")

    estilo_inst = EstiloCls()

    # prefer explicit methods if present
    if hasattr(estilo_inst, "gerar_valores"):
        vals = estilo_inst.gerar_valores()
        return list(vals)

    if hasattr(estilo_inst, "gerar"):
        vals = estilo_inst.gerar()
        return list(vals)

    if hasattr(estilo_inst, "aplicar"):
        # criar temporário Atributos e aplicar
        temp = Atributos()  # usa construtor com valores zeros ou defaults
        # if aplicar expects personagem param, call it
        estilo_inst.aplicar(temp)
        # extrai em ordem: forca,destreza,constituicao,inteligencia,sabedoria,carisma
        return [
            int(getattr(temp, "forca", 0)),
            int(getattr(temp, "destreza", 0)),
            int(getattr(temp, "constituicao", 0)),
            int(getattr(temp, "inteligencia", 0)),
            int(getattr(temp, "sabedoria", 0)),
            int(getattr(temp, "carisma", 0)),
        ]

    # fallback (shouldn't happen)
    raise RuntimeError("A classe de estilo não possui métodos compatíveis.")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip() or "SemNome"
        estilo = request.form.get("estilo")  # classico / aventureiro / heroico
        raca_key = request.form.get("raca")
        classe_key = request.form.get("classe")

        # gera os 6 valores de atributo (pode ser usado para assign)
        try:
            valores = try_generate_values_from_style(estilo)
        except Exception as e:
            return f"Erro ao gerar atributos: {e}", 500

        # Se estilo exige escolha (aventureiro ou heroico) — mostramos assign.html
        if estilo in ("aventureiro", "heroico"):
            # envia valores enumerados para assign template
            enum_vals = list(enumerate(valores, start=1))  # [(1,v1),...]
            return render_template(
                "assign.html",
                nome=nome,
                estilo=estilo,
                raca=raca_key,
                classe=classe_key,
                valores=enum_vals
            )

        # Caso contrário (classico por exemplo), atribui na ordem padrão
        # cria personagem usando Atributos como "personagem"
        personagem = Atributos(
            forca=valores[0],
            destreza=valores[1],
            constituicao=valores[2],
            inteligencia=valores[3],
            sabedoria=valores[4],
            carisma=valores[5],
        )
        personagem.nome = nome

        # associa classe e raça
        personagem.classe = CLASSES.get(classe_key, Guerreiro)()
        personagem.raca = RACAS.get(raca_key, Humano)()

        # salva JSON
        saved = save_personagem_json(personagem)
        print("Personagem salvo em:", saved)

        return render_template("summary.html", personagem=personagem)

    # GET: exibe formulário
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def create():
    """
    Rota chamada a partir de assign.html quando o usuário escolheu
    manualmente a qual atributo aplicar cada valor (aventureiro/heroico).
    Recebe selects com valores no formato "<valor>|<idx>" (como implementado em assign.html).
    """
    nome = request.form.get("nome", "").strip() or "SemNome"
    estilo = request.form.get("estilo")
    raca_key = request.form.get("raca")
    classe_key = request.form.get("classe")

    # extrai os valores escolhidos (espera campos: forca,destreza,constituicao,inteligencia,sabedoria,carisma)
    try:
        def parse_field(field_name):
            v = request.form.get(field_name)
            if not v:
                return 0
            # v format "valor|idx" -> pegar só valor
            return int(v.split("|")[0])

        personagem = Atributos(
            forca=parse_field("forca"),
            destreza=parse_field("destreza"),
            constituicao=parse_field("constituicao"),
            inteligencia=parse_field("inteligencia"),
            sabedoria=parse_field("sabedoria"),
            carisma=parse_field("carisma"),
        )
    except Exception as e:
        return f"Erro lendo valores do formulário: {e}", 400

    personagem.nome = nome
    personagem.classe = CLASSES.get(classe_key, Guerreiro)()
    personagem.raca = RACAS.get(raca_key, Humano)()

    # salva JSON
    saved = save_personagem_json(personagem)
    print("Personagem salvo em:", saved)

    return render_template("summary.html", personagem=personagem)


if __name__ == "__main__":
    app.run(debug=True)
