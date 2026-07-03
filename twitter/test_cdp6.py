# test_cdp5.py

from playwright.sync_api import sync_playwright

TEXTO = "TESTE PLAYWRIGHT CDP 🚀"

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

    print("Procurando textbox...")

    textbox = page.locator(
        '[data-testid="tweetTextarea_0"]'
    ).first

    textbox.wait_for(timeout=15000)

    print("Clicando textbox...")

    textbox.click()

    page.wait_for_timeout(1000)

    print("Digitando texto...")

    page.keyboard.type(
        TEXTO,
        delay=50
    )

    page.wait_for_timeout(2000)

    print("Salvando screenshot...")

    page.screenshot(
        path="texto_digitado.png",
        full_page=True
    )

    print("===================================")
    print("TEXTO INSERIDO COM SUCESSO")
    print("Screenshot: texto_digitado.png")
    print("NENHUMA PUBLICAÇÃO FOI FEITA")
    print("===================================")

    input(
        "\nPressione ENTER para fechar..."
    )

    page.close()
