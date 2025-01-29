from flask import Flask, request, jsonify
from playwright.async_api import async_playwright
import asyncio

app = Flask(__name__)

async def run_playwright(form_id):
    async with async_playwright() as p:
        # Launch browser with system-installed Chromium
        browser = await p.chromium.launch(headless=True, executable_path="/usr/bin/chromium")
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to the login page
        await page.goto("https://admin.typeform.com/login")

        # Enter email address
        await page.fill('input[name="email"]', "kenzomorsa@protonmail.com")

        # Click the "Continue with email" button
        await page.click('button:has-text("Continue with email")')

        # Wait for password field and enter password
        await page.fill('input[name="password"]', "FHSvQe~@,_h!4z9")

        # Press Enter instead of clicking the "Log into Typeform" button
        await page.press('input[name="password"]', "Enter")

        # Wait for the workspace page to load
        await page.wait_for_url("https://admin.typeform.com/accounts/*")

        # Navigate to the dynamic Webhooks section
        webhooks_url = f"https://admin.typeform.com/form/{form_id}/connect#/section/webhooks"
        await page.goto(webhooks_url)

        # Wait for the Webhooks page to load
        await page.wait_for_timeout(3000)
        await page.wait_for_url(webhooks_url)

        # Verify final URL
        assert "connect#/section/webhooks" in page.url

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
        is_disabled = await toggle.get_attribute("disabled")
        is_checked = await toggle.get_attribute("aria-checked")
        print(f"Toggle Disabled: {is_disabled}, Checked: {is_checked}")

        # Force click if it's off
        if is_checked == "false":
            await toggle.click(force=True)

        await browser.close()

@app.route("/run-playwright", methods=["GET"])
def run():
    form_id = request.args.get("form_id")
    if not form_id:
        return jsonify({"error": "form_id is required"}), 400

    asyncio.run(run_playwright(form_id))
    return jsonify({"message": "Playwright script executed successfully", "form_id": form_id})

if __name__ == "__main__":
    app.run()
