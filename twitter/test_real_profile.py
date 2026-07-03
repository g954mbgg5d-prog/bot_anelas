from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="/root/.config/google-chrome",
        channel="chrome",
        headless=True,
        args=["--no-sandbox"]
    )

    page = context.new_page()

    page.goto("https://x.com")

    page.wait_for_timeout(5000)

    print(page.url)

    page.screenshot(path="real_profile.png")

    context.close()
