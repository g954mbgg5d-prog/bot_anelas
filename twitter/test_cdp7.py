# test_post_real.py

from playwright.sync_api import sync_playwright

TEXTO = "flopa que passa, sua puta 😂😂"

with sync_playwright() as p:

    print("Conectando ao Chrome...")

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    context = browser.contexts[0]

    page = context.new_page()

    print("Abrindo composer...")

    page.goto(
        "https://x.com/compose/post",
        wait_until="networkidle"
    )

    page.wait_for_timeout(5000)

    textbox = page.locator(
        '[data-testid="tweetTextarea_0"]'
    ).first

    textbox.click()

    page.keyboard.type(
        TEXTO,
        delay=30
    )

    page.wait_for_timeout(2000)

    print("Procurando botão de publicação...")

    botao = page.locator(
        '[data-testid="tweetButton"]'
    ).first

    print("Publicando...")

    botao.click()

    page.wait_for_timeout(8000)

    page.screenshot(
        path="tweet_publicado.png",
        full_page=True
    )

    print("")
    print("================================")
    print("TWEET ENVIADO")
    print("Screenshot: tweet_publicado.png")
    print("================================")

    page.close()
