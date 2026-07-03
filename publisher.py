import logging
from datetime import datetime

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

CDP_URL = "http://127.0.0.1:9222"


def publicar(texto):

    page = None

    try:

        logger.info("Iniciando publicação no X")

        with sync_playwright() as p:

            browser = p.chromium.connect_over_cdp(
                CDP_URL
            )

            context = browser.contexts[0]

            page = context.new_page()

            page.goto(
                "https://x.com/compose/post",
                wait_until="networkidle"
            )

            page.wait_for_timeout(3000)

            textbox = page.locator(
                '[data-testid="tweetTextarea_0"]'
            ).first

            textbox.wait_for(timeout=15000)

            textbox.click()

            page.keyboard.type(
                texto,
                delay=20
            )

            page.wait_for_timeout(1000)

            botao = page.locator(
                '[data-testid="tweetButton"]'
            ).first

            botao.click()

            page.wait_for_timeout(5000)

            logger.info(
                "Tweet publicado com sucesso"
            )

            page.close()

            return True

    except Exception as e:

        logger.exception(
            "Erro ao publicar tweet: %s",
            e
        )

        try:

            if page:

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                page.screenshot(
                    path=f"logs/twitter_error_{timestamp}.png",
                    full_page=True
                )

        except Exception:
            pass

        return False
