import logging

logger = logging.getLogger(__name__)


def publicar(texto):

    logger.info(
        "PUBLICACAO_SIMULADA: %s",
        texto
    )

    print()
    print("=" * 80)
    print("PUBLICACAO SIMULADA")
    print("=" * 80)
    print(texto)
    print("=" * 80)
    print()

    return True
