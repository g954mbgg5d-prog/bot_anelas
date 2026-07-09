import random
import pandas as pd
import sheets

from database import obter_indices_bloqueados


# ==================================================
# MAPEAMENTO DAS PLANILHAS
# ==================================================

MAPEAMENTO = {

    "substantivos": {
        "campos": {
            "palavra": "substantivo",
            "artigo": "artigo",
            "de": "de",
            "em": "em",
        }
    },

    "verbos": {
        "campos": {
            "infinitivo": "infinitivo",
            "presente": "presente",
            "passado": "passado",
            "gerundio": "gerundio",
        }
    },

    "frases": {
        "campos": {
            "frase": "frase",
        }
    },

    "chamada": {
        "campos": {
            "chamada": "chamada",
        }
    },

    "lugares": {
        "campos": {
            "lugar": "lugar",
            "de_lugar": "de_lugar",
            "em_lugar": "em_lugar",
            "pra_lugar": "pra_lugar",
        }
    },

    "coisas": {
        "campos": {
            "coisa": "coisa",
            "artigo_coisa": "artigo_coisa",
            "um_coisa": "um_coisa",
        }
    },

    "comidas": {
        "campos": {
            "comida": "comida",
            "um_comida": "um_comida",
        }
    },

}

def limpar(valor):

    if valor is None:
        return ""

    if pd.isna(valor):
        return ""

    valor = str(valor).strip()

    if valor.lower() == "nan":
        return ""

    return valor

class SelectionManager:

    def __init__(self):

        self.usados = {}

    # ==================================================
    # ESCOLHE UMA LINHA
    # ==================================================

    def _linha(self, categoria):

        if categoria not in self.usados:
            self.usados[categoria] = []

        df = sheets.get(categoria)

        bloqueados = obter_indices_bloqueados(
            categoria
        )

        usados = set(
            self.usados[categoria]
        )

        disponiveis = [

            indice

            for indice in df.index

            if indice not in usados
            and indice not in bloqueados

        ]

        if not disponiveis:

            disponiveis = [

                indice

                for indice in df.index

                if indice not in usados

            ]

        if not disponiveis:

            raise RuntimeError(
                f"Sem itens disponíveis em '{categoria}'."
            )

        indice = random.choice(
            disponiveis
        )

        self.usados[categoria].append(
            indice
        )

        return indice, df.loc[indice]

    # ==================================================
    # ESCOLHA GENÉRICA
    # ==================================================

    def escolher(self, categoria, sufixo=""):

        indice, linha = self._linha(
            categoria
        )

        valores = {}

        mapa = MAPEAMENTO[
            categoria
        ]["campos"]

        for coluna, placeholder in mapa.items():

            valores[
                placeholder + sufixo
            ] = limpar(
                linha[coluna]
            )

        return valores, linha

    # ==================================================
    # ADJETIVO
    # ==================================================

    def escolher_adjetivo(
        self,
        artigo,
        sufixo=""
    ):

        _, linha = self._linha(
            "adjetivos"
        )

        coluna = "fem" if artigo == "a" else "masc"

        return {

            "adjetivo" + sufixo: str(
                linha[coluna]
            ).strip()

        }

    # ==================================================
    # TEMPLATE
    # ==================================================

    def template(self):

        _, linha = self._linha(
            "templates"
        )

        return str(
            linha["template"]
        ).strip()

    # ==================================================
    # COOLDOWNS
    # ==================================================

    def cooldowns(self):

        return self.usados

