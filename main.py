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
    marcar_publicado,
)

from queue_manager import (
    abastecer_fila,
    proximo_tweet,
)

from scheduler import (
    deve_publicar,
)

from publisher import (
    publicar,
)

# ==================================================
# LOGGING
# ==================================================

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

# ==================================================
# SHEETS
# ==================================================

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


# ==================================================
# LOOP
# ==================================================

def executar_ciclo():

    sincronizar_planilhas()

    total = abastecer_fila()

    logger.info(
        "Fila pendente: %s",
        total
    )

    if not deve_publicar():

        logger.info(
            "Scheduler decidiu nao publicar"
        )

        return

    tweet = proximo_tweet()

    if not tweet:

        logger.warning(
            "Nenhum tweet pendente encontrado"
        )

        return

    sucesso = publicar(
        tweet["texto"]
    )

    if not sucesso:

        logger.warning(
            "Falha na publicacao"
        )

        return

    marcar_publicado(
        tweet["id"]
    )

    logger.info(
        "Tweet publicado: id=%s",
        tweet["id"]
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
