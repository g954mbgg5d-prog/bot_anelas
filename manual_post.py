import logging
import sys

import sheets

from database import (
    init_db,
    inserir_tweet,
    registrar_cooldowns,
)

from generator import gerar_frase
from publisher import publicar


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():

    init_db()

    print("Sincronizando planilhas...")

    try:
        sheets.sync()
    except Exception as erro:
        print(f"Erro ao sincronizar planilhas: {erro}")
        sys.exit(1)

    print("Gerando tweet...")

    try:
        texto, manager = gerar_frase()
    except Exception as erro:
        print(f"Erro ao gerar tweet: {erro}")
        sys.exit(1)

    print()
    print("========================================")
    print(texto)
    print("========================================")
    print()

    print("Publicando...")

    if not publicar(texto):

        print("❌ Falha ao publicar.")
        sys.exit(1)

    inserir_tweet(texto)

    registrar_cooldowns(
        manager
    )

    print("✅ Tweet publicado com sucesso!")


if __name__ == "__main__":
    main()
