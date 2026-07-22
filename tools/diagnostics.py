from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import sqlite3
import sheets

from config import (
    DATABASE_PATH,
    COOLDOWNS,
)

from database import get_metadata

from scheduler import (
    minutos_desde_ultima_publicacao,
    chance_publicacao,
)


def main():

    print("========== BOT ANELAS ==========")

    print()

    sheets.sync()

    print("Planilhas")

    for nome in sheets.stats():

        print(f"  ✓ {nome}")

    print()

    minutos = minutos_desde_ultima_publicacao()

    chance = chance_publicacao(minutos)

    print("Scheduler")

    print(f"  Última publicação : {minutos}")

    print(f"  Chance atual      : {chance}%")

    print()

    conn = sqlite3.connect(DATABASE_PATH)

    cur = conn.cursor()

    cur.execute(

        """
        SELECT COUNT(*)

        FROM tweets
        """
    )

    total = cur.fetchone()[0]

    print(f"Tweets publicados : {total}")

    print()

    print("Cooldowns")

    cur.execute(

        """
        SELECT categoria,
               COUNT(*)

        FROM recent_items

        GROUP BY categoria

        ORDER BY categoria
        """
    )

    usados = dict(cur.fetchall())

    for categoria, cooldown in COOLDOWNS.items():

        atual = usados.get(categoria, 0)

        print(

            f"  {categoria:<15}"

            f"{atual}/{cooldown}"

        )

    conn.close()


if __name__ == "__main__":
    main()