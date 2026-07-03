from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="/root/twitter_profile",
        channel="chrome",
        headless=True,
        args=["--no-sandbox"]
    )

    page = context.new_page()

    page.goto(
        "https://x.com/home",
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    print("URL:", page.url)
    print("TITLE:", page.title())

    page.screenshot(path="home_test.png")

    context.close()
