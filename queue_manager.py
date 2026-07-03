from config import (
    MIN_QUEUE_SIZE,
    QUEUE_BATCH_SIZE,
)

from generator import gerar_frase

from database import (
    inserir_tweet,
    contar_pending,
    obter_proximo_pendente,
)


def gerar_lote(
    quantidade=QUEUE_BATCH_SIZE
):

    adicionados = 0

    for _ in range(quantidade):

        texto = gerar_frase()

        if inserir_tweet(texto):
            adicionados += 1

    return adicionados


def abastecer_fila():

    total = contar_pending()

    while total < MIN_QUEUE_SIZE:

        gerar_lote()

        total = contar_pending()

    return total


def proximo_tweet():

    return obter_proximo_pendente()
