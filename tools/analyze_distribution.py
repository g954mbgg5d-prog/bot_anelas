from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from collections import Counter
import time

import sheets

from database import (
    init_db,
    gerar_hash,
)

from generator import gerar_frase


TOTAL = 10000


def main():

    print("=" * 60)
    print("BOT ANELAS - DISTRIBUTION ANALYZER")
    print("=" * 60)
    print()

    init_db()
    sheets.sync()

    hashes = set()

    templates = Counter()
    categorias = Counter()

    repetidos = 0

    inicio = time.perf_counter()

    for i in range(TOTAL):

        texto, manager = gerar_frase()

        h = gerar_hash(texto)

        if h in hashes:
            repetidos += 1
        else:
            hashes.add(h)

        cooldowns = manager.cooldowns()

        for categoria, indices in cooldowns.items():

            categorias[categoria] += len(indices)

            if categoria == "templates":
                templates.update(indices)

        if (i + 1) % 1000 == 0:

            print(f"{i+1}/{TOTAL}")

    tempo = time.perf_counter() - inicio

    print()
    print("=" * 60)
    print("RESULTADO")
    print("=" * 60)

    print(f"Tweets gerados          : {TOTAL}")
    print(f"Tweets únicos           : {len(hashes)}")
    print(f"Colisões de hash        : {repetidos}")
    print(f"Tempo total             : {tempo:.2f}s")
    print(f"Média por tweet         : {tempo/TOTAL:.5f}s")

    print()
    print("=" * 60)
    print("UTILIZAÇÃO POR CATEGORIA")
    print("=" * 60)

    for categoria, total in sorted(categorias.items()):

        media = total / TOTAL

        print(
            f"{categoria:<15}"
            f"{total:>8} usos"
            f" ({media:.2f}/tweet)"
        )

    print()
    print("=" * 60)
    print("TOP 20 TEMPLATES")
    print("=" * 60)

    for indice, vezes in templates.most_common(20):

        print(
            f"Template {indice:<4}"
            f"{vezes:>6} vezes"
        )

    print()
    print("=" * 60)
    print("BOTTOM 20 TEMPLATES")
    print("=" * 60)

    menos = sorted(
        templates.items(),
        key=lambda x: x[1]
    )[:20]

    for indice, vezes in menos:

        print(
            f"Template {indice:<4}"
            f"{vezes:>6} vezes"
        )


if __name__ == "__main__":
    main()