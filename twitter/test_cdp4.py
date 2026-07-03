from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    page = browser.contexts[0].new_page()

    page.goto("https://x.com/compose/post")

    page.wait_for_timeout(5000)

    elementos = page.locator("[data-testid]").evaluate_all(
        """
        els => [...new Set(
            els.map(e => e.getAttribute('data-testid'))
        )]
        """
    )

    for e in elementos:
        print(e)
