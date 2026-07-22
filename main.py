import logging
import time
from datetime import datetime, timedelta

import sheets

from config import (
    LOOP_INTERVAL_SECONDS,
    SHEETS_SYNC_INTERVAL_MINUTES,
    LOG_LEVEL,
    LOGS_DIR,
)

from database import (
    init_db,
    registrar_cooldowns,
)

from queue_manager import (
    gerar_tweet,
    salvar_publicado,
)

from scheduler import (
    deve_publicar,
)

from publisher import (
    publicar,
)


LOGS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            LOGS_DIR / "bot.log"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

ultima_sincronizacao = None


def sincronizar_planilhas():

    global ultima_sincronizacao

    agora = datetime.utcnow()

    if ultima_sincronizacao is None:

        logger.info(
            "Primeira sincronizacao das planilhas"
        )

        sheets.sync()

        ultima_sincronizacao = agora

        return

    limite = (
        ultima_sincronizacao
        + timedelta(
            minutes=SHEETS_SYNC_INTERVAL_MINUTES
        )
    )

    if agora >= limite:

        logger.info(
            "Atualizando planilhas"
        )

        sheets.sync()

        ultima_sincronizacao = agora


def executar_ciclo():

    sincronizar_planilhas()

    if not deve_publicar():

        logger.info(
            "Scheduler decidiu nao publicar"
        )

        return

    texto, manager = gerar_tweet()

    logger.info(
        "Tweet gerado: %s",
        texto
    )

    if not publicar(texto):

        logger.warning(
            "Falha na publicacao"
        )

        return

    salvar_publicado(texto)

    registrar_cooldowns(
        manager
    )

    logger.info(
        "Tweet publicado."
    )


def main():

    logger.info(
        "Inicializando BOT ANELAS"
    )

    init_db()

    while True:

        try:

            executar_ciclo()

        except Exception:

            logger.exception(
                "Erro durante ciclo principal"
            )

        time.sleep(
            LOOP_INTERVAL_SECONDS
        )


if __name__ == "__main__":
    main()
