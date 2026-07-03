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

    print("URL:", page.url)

    content = page.content()

    if "Post" in content or "What's happening" in content or "For you" in content:
        print("POSSIVELMENTE LOGADO")

    if "Sign in" in content or "Log in" in content:
        print("POSSIVELMENTE DESLOGADO")

    page.screenshot(path="home_test.png")

    context.close()
