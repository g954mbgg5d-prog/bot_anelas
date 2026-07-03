import pandas as pd

from config import (
    SHEET_ID,
    GIDS,
)

# cache em memória
_cache = {}


def _url_csv(gid):

    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/export?format=csv&gid={gid}"
    )


def carregar_aba(gid):

    return pd.read_csv(
        _url_csv(gid)
    )


def sync():

    global _cache

    novo_cache = {}

    for nome, gid in GIDS.items():

        novo_cache[nome] = carregar_aba(gid)

    _cache = novo_cache

    return True


def get(nome):

    if nome not in _cache:

        raise RuntimeError(
            f"Aba '{nome}' não carregada. "
            f"Execute sheets.sync() primeiro."
        )

    return _cache[nome]


def is_loaded():

    return len(_cache) > 0


def stats():

    resultado = {}

    for nome, df in _cache.items():

        resultado[nome] = len(df)

    return resultado
