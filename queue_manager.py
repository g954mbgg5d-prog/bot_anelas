from database import (
    inserir_tweet,
    tweet_existe,
)

from generator import gerar_frase


def gerar_tweet():

    tentativas = 0

    while True:

        tentativas += 1

        texto, manager = gerar_frase()

        if tweet_existe(texto):

            if tentativas % 50 == 0:

                print(
                    f"Ja foram feitas {tentativas} tentativas para gerar um tweet inedito..."
                )

            continue

        return texto, manager


def salvar_publicado(texto):

    inserir_tweet(
        texto,
        status="published"
    )
