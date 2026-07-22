from pathlib import Path
import sys
import re
from collections import Counter
import traceback

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import sheets

from database import init_db
from generator import gerar_frase


TOTAL = 5000

PADROES = {
    "nan": r"\bnan\b",
    "none": r"\bnone\b",
    "placeholder": r"\{[a-zA-Z0-9_]+\}",
}


def banner(titulo):

    print()
    print("=" * 80)
    print(titulo)
    print("=" * 80)


def registrar_erro(
    nome,
    texto,
    manager,
    erros,
    exemplos,
):

    erros[nome] += 1

    if nome not in exemplos:

        exemplos[nome] = (
            texto,
            manager.cooldowns(),
        )


def main():

    banner("BOT ANELAS - CONTENT CHECK")

    init_db()

    sheets.sync()

    erros = Counter()

    exemplos = {}

    for i in range(TOTAL):

        try:

            texto, manager = gerar_frase()

        except Exception:

            banner("ERRO FATAL")

            traceback.print_exc()

            return

        #
        # Regex
        #

        for nome, padrao in PADROES.items():

            if re.search(
                padrao,
                texto,
                flags=re.IGNORECASE,
            ):

                registrar_erro(
                    nome,
                    texto,
                    manager,
                    erros,
                    exemplos,
                )

        #
        # Tweet vazio
        #

        if not texto.strip():

            registrar_erro(
                "vazio",
                texto,
                manager,
                erros,
                exemplos,
            )

        #
        # Limite do X
        #

        if len(texto) > 280:

            registrar_erro(
                "280+",
                texto,
                manager,
                erros,
                exemplos,
            )

        #
        # Espaços duplos
        #

        if "  " in texto:

            registrar_erro(
                "espacos_duplos",
                texto,
                manager,
                erros,
                exemplos,
            )

        #
        # Quebra de linha
        #

        if "\n" in texto:

            registrar_erro(
                "quebra_linha",
                texto,
                manager,
                erros,
                exemplos,
            )

        #
        # Tab
        #

        if "\t" in texto:

            registrar_erro(
                "tab",
                texto,
                manager,
                erros,
                exemplos,
            )

        #
        # Espaço no começo
        #

        if texto.startswith(" "):

            registrar_erro(
                "espaco_inicio",
                texto,
                manager,
                erros,
                exemplos,
            )

        #
        # Espaço no fim
        #

        if texto.endswith(" "):

            registrar_erro(
                "espaco_fim",
                texto,
                manager,
                erros,
                exemplos,
            )

        #
        # Progresso
        #

        if (i + 1) % 500 == 0:

            print(f"{i + 1}/{TOTAL}")

    banner("RESULTADO")

    if not erros:

        print("✅ Nenhum problema encontrado.")
        print(f"Tweets analisados: {TOTAL}")
        return

    print(f"Tweets analisados: {TOTAL}")

    for problema in sorted(erros):

        print()

        print(f"Problema    : {problema}")
        print(f"Ocorrências : {erros[problema]}")

        texto, cooldowns = exemplos[problema]

        print()

        print("Exemplo:")

        print(texto)

        print()

        print("Cooldowns utilizados:")

        for categoria, indices in cooldowns.items():

            print(
                f"  {categoria:<15}{indices}"
            )


if __name__ == "__main__":
    main()