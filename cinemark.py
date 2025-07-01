import asyncio
import requests
from playwright.async_api import async_playwright
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_IDS = [
    7870007969,
    7984014685,
    7750213640
]
MESSAGE = "✅ ¡La película 'Los 4 Fantásticos' YA está disponible en Cinemark Mallplaza Trujillo! 🎬🍿"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.cinemark-peru.com/movie?tag=744&corporate_film_id=104393&coming_soon=false&pelicula=los-4-fantasticos&cine=cinemark_mallplaza_trujillo")

        try:
            await page.wait_for_selector(".movie-error-alert", timeout=5000)
            print("❌ La película aún NO está disponible")
        except:
            print("✅ La película YA está disponible")
            for chat_id in CHAT_IDS:
                send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": MESSAGE
                }
                requests.post(send_url, data=payload)
                print(f"Mensaje enviado a chat_id {chat_id}")

        await browser.close()

asyncio.run(run())