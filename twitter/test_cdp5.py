# test_post.py

from playwright.sync_api import sync_playwright

TEXTO = "Teste automático via Playwright + CDP 🚀"

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    context = browser.contexts[0]

    page = context.new_page()

    page.goto("https://x.com/compose/post")

    page.wait_for_selector(
        '[data-testid="tweetTextarea_0"]',
        timeout=15000
    )

    page.locator(
        '[data-testid="tweetTextarea_0"]'
    ).click()

    page.keyboard.type(TEXTO)

    page.wait_for_timeout(2000)

    print("Texto digitado")

    page.locator(
        '[data-testid="tweetButton"]'
    ).click()

    page.wait_for_timeout(5000)

    print("PUBLICADO")
