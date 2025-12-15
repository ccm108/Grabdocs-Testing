from playwright.sync_api import sync_playwright

def create_calendar_event():
    with sync_playwright() as p:
        # Launch Firefox browser
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Set global default timeout to 6 minutes (360000 ms)
        page.set_default_timeout(360000)

        # --- Login ---
        page.goto("https://app.grabdocs.com/login")
        page.locator("#username").fill("chrism4321")
        page.locator("#password").fill("GRABDOCS_PASS")
        page.locator("text=Sign in").click()

        # --- 2FA Step (manual) ---
        print("Please enter your 2FA code manually in the browser and click 'Verify Code'.")
        page.wait_for_selector("#optCode")
        page.pause()  # Pauses until you resume in the inspector

        # Wait until calendar page loads
        page.wait_for_url("https://app.grabdocs.com/calendar")

        # --- Calendar / Event Creation ---
        page.locator("text=Calendar").click()
        page.locator("text=New Event").click()

        # Fill in event details
        page.locator("input[placeholder='Team Meeting, Client Call, etc.']").fill("GrabDocs Project Presentation")
        page.locator("input[type='date']").fill("2025-12-16")
        page.locator("input[type='time']").fill("19:30")
        page.locator("select").select_option("180")  # 3 hours
        page.locator("input[placeholder='Location']").fill("Computer Science Building")

        # Submit event
        page.locator("text=Create Event").click()

        # Verify event appears on calendar
        page.wait_for_selector("text=GrabDocs Project Presentation")
        print("Event created successfully!")

        # Close browser
        browser.close()

        # --- Delete Event (Cleanup) ---
# NOTE: This step is best-effort and may require UI-specific selectors

    try:
        # Click the event on the calendar
        page.wait_for_selector("text=GrabDocs Project Presentation", timeout=10000)
        page.locator("text=GrabDocs Project Presentation").click()
    
        # Open event options / menu
        page.wait_for_selector("text=Delete", timeout=5000)
        page.locator("text=Delete").click()
    
        # Confirm deletion
        page.wait_for_selector("text=Confirm", timeout=5000)
        page.locator("text=Confirm").click()
    
        print("Event deleted successfully.")
    
    except Exception as e:
        print("Delete event step skipped or failed (non-blocking):", e)

def test_calendar_event():
    create_calendar_event()

if __name__ == "__main__":
    test_calendar_event()
