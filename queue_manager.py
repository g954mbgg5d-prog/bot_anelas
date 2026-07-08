from config import MAX_QUEUE_SIZE

from generator import gerar_frase

from database import (
    inserir_tweet,
    contar_pending,
    obter_proximo_pendente,
)


def abastecer_fila():

    total = contar_pending()

    faltam = MAX_QUEUE_SIZE - total

    if faltam <= 0:
        return total

    for _ in range(faltam):

        texto = gerar_frase()

        inserir_tweet(texto)

    return contar_pending()


def proximo_tweet():

    return obter_proximo_pendente()
