from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="/root/bot_anelas/twitter/session/playwright_profile",
        headless=False,
        args=["--no-sandbox"]
    )

    page = context.new_page()

    page.goto("https://x.com")

    print("")
    print("FAÇA LOGIN MANUALMENTE")
    print("DEPOIS VOLTE AQUI E APERTE ENTER")
    print("")

    input()

    context.close()
