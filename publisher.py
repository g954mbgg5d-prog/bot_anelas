import logging
import os

import tweepy
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)


consumer_key = os.getenv("X_CONSUMER_KEY")
consumer_secret = os.getenv("X_CONSUMER_SECRET")
access_token = os.getenv("X_ACCESS_TOKEN")
access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")


client = None


if all([
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
]):

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )


def publicar(texto):

    try:

        logger.info(
            "Iniciando publicacao no X via API"
        )

        if client is None:

            raise RuntimeError(
                "Credenciais da API do X "
                "nao encontradas no .env"
            )

        response = client.create_tweet(
            text=texto
        )

        tweet_id = response.data["id"]

        logger.info(
            "Tweet publicado com sucesso "
            "via API. ID: %s",
            tweet_id
        )

        return True

    except Exception as erro:

        logger.exception(
            "Erro ao publicar tweet via API: %s",
            erro
        )

        return False
