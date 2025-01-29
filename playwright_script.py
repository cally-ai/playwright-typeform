from flask import Flask, request, jsonify
from playwright.async_api import async_playwright
import asyncio
import os

# ✅ Ensure Playwright uses built-in Chromium
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

app = Flask(__name__)

async def run_playwright(form_id):
    async with async_playwright() as p:
        browser = None  # ✅ Ensure browser is initialized
        try:
            # ✅ Launch Chromium with necessary flags for cloud execution
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

            print(f"🚀 Running Playwright for form: {form_id}")

            # ✅ Navigate to the login page
            await page.goto("https://admin.typeform.com/login", timeout=30000)

            # ✅ Enter email and login
            await page.fill('input[name="email"]', "kenzomorsa@protonmail.com")
            await page.click('button:has-text("Continue with email")')
            await page.wait_for_selector('input[name="password"]', timeout=10000)
            await page.fill('input[name="password"]', "FHSvQe~@,_h!4z9")
            await page.press('input[name="password"]', "Enter")

            # ✅ Wait for successful login
            await page.wait_for_url("https://admin.typeform.com/accounts/*", timeout=30000)

            # ✅ Navigate to Webhooks Section (Dynamic `form_id`)
            webhooks_url = f"https://admin.typeform.com/form/{form_id}/connect#/section/webhooks"
            await page.goto(webhooks_url, timeout=30000)

            # ✅ Wait for the Webhooks page to load
            await page.wait_for_url(webhooks_url, timeout=30000)

            # ✅ Click "Add a webhook" button
            await page.wait_for_selector('button:has-text("Add a webhook")', timeout=10000)
            await page.click('button:has-text("Add a webhook")')

            # ✅ Enter Webhook URL
            await page.wait_for_selector("text=Add a webhook", timeout=10000)
            await page.fill('input[type="text"]', "https://hook.eu2.make.com/5rwgsndddpj6efnt8tj46u1nk9iwao0y")

            # ✅ Click "Save webhook"
            await page.click('button:has-text("Save webhook")')

            # ✅ Wait for Webhook to appear in list
            await page.wait_for_selector('span[data-qa="webhook-url"]', timeout=10000)

            # ✅ Toggle Webhook if OFF
            toggle = page.locator('button[role="switch"]')
            is_checked = await toggle.get_attribute("aria-checked")
            print(f"🔄 Toggle Status Before: {is_checked}")

            if is_checked == "false":
                await toggle.click(force=True)
                print(f"✅ Webhook enabled for form {form_id}")

        except Exception as e:
            print(f"❌ Playwright Execution Failed: {str(e)}")

        finally:
            if browser:
                await browser.close()


@app.route("/run-playwright", methods=["GET"])
def run():
    form_id = request.args.get("form_id")
    if not form_id:
        return jsonify({"error": "form_id is required"}), 400

    print(f"📡 Received request to run Playwright for form {form_id}")

    # ✅ Handle Async Execution Properly
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(run_playwright(form_id))
        else:
            loop.run_until_complete(run_playwright(form_id))
    except RuntimeError:
        asyncio.run(run_playwright(form_id))

    return jsonify({"message": "Playwright script is running in the background", "form_id": form_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
