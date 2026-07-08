import logging
import random

import pandas as pd

import sheets


logger = logging.getLogger(__name__)

MAX_TENTATIVAS = 10


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


def gerar_valores():

    substantivos = sheets.get("substantivos")
    adjetivos = sheets.get("adjetivos")
    verbos = sheets.get("verbos")
    frases = sheets.get("frases")
    chamadas = sheets.get("chamada")

    valores = {}

    for i in range(1, 6):

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

    return valores


def gerar_frase():

    templates = sheets.get("templates")

    ultimo_erro = None

    for tentativa in range(1, MAX_TENTATIVAS + 1):

        template = limpar(
            linha_aleatoria(templates)["template"]
        )

        try:

            valores = gerar_valores()

            resultado = template.format(
                **valores
            )

            resultado = " ".join(
                resultado.split()
            )

            if not resultado:
                raise ValueError(
                    "Resultado vazio"
                )

            return resultado

        except (
            KeyError,
            ValueError,
            IndexError,
        ) as erro:

            ultimo_erro = erro

            logger.warning(
                "Template invalido ignorado "
                "(tentativa %s/%s): %r | erro: %s",
                tentativa,
                MAX_TENTATIVAS,
                template,
                erro,
            )

    raise RuntimeError(
        "Nao foi possivel gerar uma frase valida "
        f"apos {MAX_TENTATIVAS} tentativas. "
        f"Ultimo erro: {ultimo_erro}"
    )
