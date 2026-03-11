from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.linkedin.com/login", timeout=60000)

    print("≡ƒæë Log in manually in the opened browser")
    print("≡ƒæë Wait until LinkedIn home page fully loads")

    page.wait_for_timeout(60000)  # 60 seconds buffer

    context.storage_state(path="linkedin_cookies.json")
    print("Γ£à Cookies saved to linkedin_cookies.json")

    browser.close()
