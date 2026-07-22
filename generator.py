import logging
import re

from config import MAX_TEMPLATE_ATTEMPTS

from selection_manager import SelectionManager


logger = logging.getLogger(__name__)

PLACEHOLDER_RE = re.compile(r"\{([a-z_]+\d*)\}")


# placeholder -> categoria
CATEGORIAS = {

    "substantivo": "substantivos",

    "infinitivo": "verbos",
    "presente": "verbos",
    "passado": "verbos",
    "gerundio": "verbos",

    "frase": "frases",

    "chamada": "chamada",

    "lugar": "lugares",
    "de_lugar": "lugares",
    "em_lugar": "lugares",
    "pra_lugar": "lugares",

    "coisa": "coisas",
    "artigo_coisa": "coisas",
    "um_coisa": "coisas",

    "comida": "comidas",
    "um_comida": "comidas",
}


def dividir_placeholder(nome):

    m = re.match(
        r"(.+?)(\d*)$",
        nome
    )

    base = m.group(1)
    indice = m.group(2)

    return base, indice


def gerar_frase():

    ultimo_erro = None

    for tentativa in range(MAX_TEMPLATE_ATTEMPTS):

        manager = SelectionManager()

        try:

            template = manager.template()

            placeholders = set(
                PLACEHOLDER_RE.findall(
                    template
                )
            )

            valores = {}

            grupos = {}

            #
            # AGRUPA PLACEHOLDERS
            #

            for placeholder in placeholders:

                base, indice = dividir_placeholder(
                    placeholder
                )

                grupos.setdefault(
                    indice,
                    set()
                ).add(base)

            #
            # PROCESSA CADA GRUPO
            #

            for indice, bases in grupos.items():

                sufixo = indice

                #
                # SUBSTANTIVOS
                #

                if (
                    "substantivo"
                    in bases
                ):

                    dados, linha = manager.escolher(
                        "substantivos",
                        sufixo
                    )

                    valores.update(
                        dados
                    )

                    if (
                        "adjetivo"
                        in bases
                    ):

                        valores.update(

                            manager.escolher_adjetivo(
                                linha["artigo"],
                                sufixo
                            )

                        )

                #
                # VERBOS
                #

                if any(

                    b in bases

                    for b in [

                        "infinitivo",
                        "presente",
                        "passado",
                        "gerundio",

                    ]

                ):

                    dados, _ = manager.escolher(
                        "verbos",
                        sufixo
                    )

                    valores.update(
                        dados
                    )

                #
                # FRASES
                #

                if "frase" in bases:

                    dados, _ = manager.escolher(
                        "frases",
                        sufixo
                    )

                    valores.update(
                        dados
                    )

                #
                # CHAMADAS
                #

                if "chamada" in bases:

                    dados, _ = manager.escolher(
                        "chamada",
                        sufixo
                    )

                    valores.update(
                        dados
                    )

                #
                # LUGARES
                #

                if any(

                    b in bases

                    for b in [

                        "lugar",
                        "de_lugar",
                        "em_lugar",
                        "pra_lugar",

                    ]

                ):

                    dados, _ = manager.escolher(
                        "lugares",
                        sufixo
                    )

                    valores.update(
                        dados
                    )

                #
                # COISAS
                #

                if any(

                    b in bases

                    for b in [

                        "coisa",
                        "artigo_coisa",
                        "um_coisa",

                    ]

                ):

                    dados, _ = manager.escolher(
                        "coisas",
                        sufixo
                    )

                    valores.update(
                        dados
                    )

                #
                # COMIDAS
                #

                if any(

                    b in bases

                    for b in [

                        "comida",
                        "um_comida",

                    ]

                ):

                    dados, _ = manager.escolher(
                        "comidas",
                        sufixo
                    )

                    valores.update(
                        dados
                    )

            texto = template.format(
                **valores
            )

            texto = " ".join(
                texto.split()
            )

            if not texto:

                raise RuntimeError(
                    "Texto vazio."
                )

            return (
                texto,
                manager
            )

        except Exception as erro:

            ultimo_erro = erro

            logger.warning(
                "Template inválido ignorado: %r | erro: %s",
                template,
                erro,
            )

    raise RuntimeError(
        ultimo_erro
    )

