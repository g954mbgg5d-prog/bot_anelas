from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="/root/twitter_profile",
        channel="chrome",
        headless=True,
        args=["--no-sandbox"]
    )

    page = context.new_page()

    page.goto("https://x.com/home", wait_until="networkidle")

    print("URL FINAL:", page.url)

    try:
        print("TITULO:", page.title())
    except:
        pass

    context.close()
