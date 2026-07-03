from playwright.sync_api import sync_playwright

texto = "Teste automático via Playwright + CDP"

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    page = browser.contexts[0].new_page()

    page.goto("https://x.com/compose/post")

    page.wait_for_timeout(3000)

    page.locator('div[role="textbox"]').fill(texto)

    page.wait_for_timeout(2000)

    page.screenshot(path="antes_publicar.png")

    print("Tweet preenchido")
