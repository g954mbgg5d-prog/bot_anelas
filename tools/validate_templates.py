from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import sheets

from database import init_db
from generator import gerar_frase


TOTAL = 1000


def main():

    init_db()

    sheets.sync()

    print(f"Validando {TOTAL} gerações...")

    erros = 0

    for _ in range(TOTAL):

        try:

            gerar_frase()

        except Exception as erro:

            erros += 1

            print(erro)

    print()

    print(f"Erros fatais: {erros}")

    if erros == 0:

        print("✅ Todos os templates passaram.")


if __name__ == "__main__":
    main()