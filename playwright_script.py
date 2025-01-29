from flask import Flask, request, jsonify
from playwright.async_api import async_playwright
import asyncio
import os

# Ensure Playwright uses its built-in Chromium
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

app = Flask(__name__)

async def run_playwright(form_id):
    async with async_playwright() as p:
        # Launch the browser with correct flags for cloud execution
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to the login page
            await page.goto("https://admin.typeform.com/login", timeout=15000)

            # Enter email address
            await page.fill('input[name="email"]', "kenzomorsa@protonmail.com")

            # Click "Continue with email" button
            await page.click('button:has-text("Continue with email")')

            # Wait for password field and enter password
            await page.fill('input[name="password"]', "FHSvQe~@,_h!4z9")

            # Press Enter instead of clicking "Log into Typeform"
            await page.press('input[name="password"]', "Enter")

            # Wait for the workspace page to load
            await page.wait_for_url("https://admin.typeform.com/accounts/*", timeout=20000)

            # Navigate to the Webhooks section (dynamic form_id)
            webhooks_url = f"https://admin.typeform.com/form/{form_id}/connect#/section/webhooks"
            await page.goto(webhooks_url, timeout=15000)

            # Ensure the Webhooks page fully loads
            await page.wait_for_url(webhooks_url, timeout=20000)

            # Click "Add a webhook" button
            await page.click('button:has-text("Add a webhook")')

            # Wait for modal and enter webhook URL
            await page.wait_for_selector("text=Add a webhook")
            await page.fill('input[type="text"]', "https://hook.eu2.make.com/5rwgsndddpj6efnt8tj46u1nk9iwao0y")

            # Click "Save webhook" button
            await page.click('button:has-text("Save webhook")')

            # Wait for webhook list to update
            await page.wait_for_selector('span[data-qa="webhook-url"]')

            # Locate the webhook toggle button
            toggle = page.locator('button[role="switch"]')

            # Log its attributes
            is_checked = await toggle.get_attribute("aria-checked")
            print(f"Toggle Checked: {is_checked}")

            # Force click if it's off
            if is_checked == "false":
                await toggle.click(force=True)

            print(f"✅ Successfully set up webhook for form {form_id}")

        except Exception as e:
            print(f"❌ Error running Playwright: {e}")

        finally:
            await browser.close()

@app.route("/run-playwright", methods=["GET"])
def run():
    form_id = request.args.get("form_id")
    if not form_id:
        return jsonify({"error": "form_id is required"}), 400

    # Fix: Run Playwright script using a new asyncio event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_playwright(form_id))
    
    return jsonify({"message": "Playwright script executed successfully", "form_id": form_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
