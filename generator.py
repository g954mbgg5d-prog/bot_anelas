import re
import random
import pandas as pd

import sheets


def limpar(valor):

    if pd.isna(valor):
        return ""

    return str(valor).strip()


def nome_variavel(base, indice):

    if indice == 1:
        return base

    return f"{base}{indice}"


def linha_aleatoria(df):

    return df.sample().iloc[0]


def gerar_frase():

    substantivos = sheets.get("substantivos")
    adjetivos = sheets.get("adjetivos")
    verbos = sheets.get("verbos")
    frases = sheets.get("frases")
    chamadas = sheets.get("chamada")
    templates = sheets.get("templates")

    template = (
        linha_aleatoria(templates)["template"]
    )

    variaveis = set(
        re.findall(
            r"\{([a-zA-Z0-9_]+)\}",
            template
        )
    )

    valores = {}

    max_sub = 5

    for i in range(1, max_sub + 1):

        sub = linha_aleatoria(substantivos)
        adj = linha_aleatoria(adjetivos)

        artigo = limpar(sub["artigo"])

        if artigo == "a":
            adjetivo = limpar(adj["fem"])
        else:
            adjetivo = limpar(adj["masc"])

        valores[nome_variavel("artigo", i)] = artigo
        valores[nome_variavel("substantivo", i)] = limpar(
            sub["palavra"]
        )
        valores[nome_variavel("adjetivo", i)] = adjetivo
        valores[nome_variavel("de", i)] = limpar(
            sub["de"]
        )
        valores[nome_variavel("em", i)] = limpar(
            sub["em"]
        )

    for i in range(1, 6):

        verbo = linha_aleatoria(verbos)

        valores[nome_variavel("infinitivo", i)] = limpar(
            verbo["infinitivo"]
        )

        valores[nome_variavel("presente", i)] = limpar(
            verbo["presente"]
        )

        valores[nome_variavel("passado", i)] = limpar(
            verbo["passado"]
        )

        valores[nome_variavel("gerundio", i)] = limpar(
            verbo["gerundio"]
        )

    for i in range(1, 6):

        frase = linha_aleatoria(frases)

        valores[nome_variavel("frase", i)] = limpar(
            frase["frase"]
        )

    for i in range(1, 6):

        chamada = linha_aleatoria(chamadas)

        valores[nome_variavel("chamada", i)] = limpar(
            chamada["chamada"]
        )

    try:

        resultado = template.format(
            **valores
        )

    except KeyError as e:

        raise RuntimeError(
            f"Template inválido. Variável ausente: {e}"
        )

    return " ".join(
        resultado.split()
    )
