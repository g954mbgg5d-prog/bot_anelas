import logging
import os

import tweepy
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)


def publicar(texto):
    try:
        logger.info("Iniciando publicação no X via API")

        consumer_key = os.getenv("X_CONSUMER_KEY")
        consumer_secret = os.getenv("X_CONSUMER_SECRET")
        access_token = os.getenv("X_ACCESS_TOKEN")
        access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

        if not all([
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret,
        ]):
            raise RuntimeError(
                "Credenciais da API do X não encontradas no .env"
            )

        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        response = client.create_tweet(text=texto)

        tweet_id = response.data["id"]

        logger.info(
            "Tweet publicado com sucesso via API. ID: %s",
            tweet_id
        )

        return True

    except Exception as e:
        logger.exception(
            "Erro ao publicar tweet via API: %s",
            e
        )

        return False
