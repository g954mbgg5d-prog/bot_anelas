import re
import pandas as pd
from flask import Flask

app = Flask(__name__)

SHEET_ID = "1Gad0WkvXNqMTcFnFlTzheTYSL42qNmZP"

GIDS = {
    "substantivos": "770008533",
    "adjetivos": "650797730",
    "verbos": "1308759085",
    "frases": "376019489",
    "chamada": "595278995",
    "templates": "1351279715",
}


def carregar_aba(gid):
    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/export?format=csv&gid={gid}"
    )
    return pd.read_csv(url)


def limpar(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def nome_variavel(base, indice):
    return base if indice == 1 else f"{base}{indice}"


def gerar_frase():

    substantivos = carregar_aba(GIDS["substantivos"])
    adjetivos = carregar_aba(GIDS["adjetivos"])
    verbos = carregar_aba(GIDS["verbos"])
    frases = carregar_aba(GIDS["frases"])
    chamadas = carregar_aba(GIDS["chamada"])
    templates = carregar_aba(GIDS["templates"])

    template = templates.sample().iloc[0]["template"]

    variaveis = set(
        re.findall(r"\{([a-zA-Z0-9_]+)\}", template)
    )

    valores = {}

    max_sub = 5

    for i in range(1, max_sub + 1):

        sub = substantivos.sample().iloc[0]
        adj = adjetivos.sample().iloc[0]

        artigo = limpar(sub["artigo"])

        if artigo == "a":
            adjetivo = limpar(adj["fem"])
        else:
            adjetivo = limpar(adj["masc"])

        valores[nome_variavel("artigo", i)] = artigo
        valores[nome_variavel("substantivo", i)] = limpar(sub["palavra"])
        valores[nome_variavel("adjetivo", i)] = adjetivo
        valores[nome_variavel("de", i)] = limpar(sub["de"])
        valores[nome_variavel("em", i)] = limpar(sub["em"])

    for i in range(1, 6):

        verbo = verbos.sample().iloc[0]

        valores[nome_variavel("infinitivo", i)] = limpar(verbo["infinitivo"])
        valores[nome_variavel("presente", i)] = limpar(verbo["presente"])
        valores[nome_variavel("passado", i)] = limpar(verbo["passado"])
        valores[nome_variavel("gerundio", i)] = limpar(verbo["gerundio"])

    for i in range(1, 6):

        frase = frases.sample().iloc[0]

        valores[nome_variavel("frase", i)] = limpar(
            frase["frase"]
        )

    for i in range(1, 6):

        chamada = chamadas.sample().iloc[0]

        valores[nome_variavel("chamada", i)] = limpar(
            chamada["chamada"]
        )

    resultado = template.format(**valores)

    return " ".join(resultado.split())


@app.route("/")
def home():

    frase = gerar_frase()

    return f"""
    <html>
    <body style="
        font-family: sans-serif;
        max-width: 700px;
        margin: 50px auto;
        padding: 20px;
    ">
        <h1>BOT ANELAS</h1>

        <div style="
            border: 1px solid #ccc;
            padding: 20px;
            font-size: 24px;
            margin-bottom: 20px;
        ">
            {frase}
        </div>

        <button onclick="window.location.reload()">
            Gerar outro
        </button>
    </body>
    </html>
    """

import os

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080))
)
