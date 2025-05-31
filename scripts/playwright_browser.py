from playwright.sync_api import sync_playwright

def run(query=""):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True if you don't want a UI
        page = browser.new_page()
        page.goto("https://www.youtube.com")

        try:
            # Wait for the search bar to be ready using a broader CSS selector
            page.wait_for_selector("input[placeholder='Search']", timeout=15000)
            page.fill("input[placeholder='Search']", query)
            page.keyboard.press("Enter")
            print(f"🔍 Searched for: {query}")
        except Exception as e:
            browser.close()
            return f"Failed to locate or interact with the search input: {e}"

        try:
            # Wait for results and click the first video
            page.wait_for_selector("ytd-video-renderer a#thumbnail", timeout=10000)
            page.click("ytd-video-renderer a#thumbnail")
            print("▶️ Clicked on the first video.")
        except Exception as e:
            browser.close()
            return f" Search succeeded, but video click failed: {e}"

        page.wait_for_timeout(5000)
        browser.close()
        return " Successfully completed YouTube search and video open."
