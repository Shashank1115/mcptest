from playwright.sync_api import sync_playwright

def open_website_and_search(url="https://www.google.com", query="OpenAI"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.fill("input[name='q']", query)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

        page.screenshot(path="search_result.png")
        browser.close()
        return "Search completed and screenshot saved."
