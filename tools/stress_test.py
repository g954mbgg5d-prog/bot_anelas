from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import time
import sheets

from database import init_db
from generator import gerar_frase


TOTAL = 5000


def main():

    init_db()

    sheets.sync()

    inicio = time.perf_counter()

    for i in range(TOTAL):

        gerar_frase()

        if i % 500 == 0:

            print(f"{i}/{TOTAL}")

    tempo = time.perf_counter() - inicio

    print()

    print("======== RESULTADO ========")

    print(f"Tweets gerados : {TOTAL}")

    print(f"Tempo total    : {tempo:.2f}s")

    print(f"Média          : {tempo/TOTAL:.5f}s")


if __name__ == "__main__":
    main()