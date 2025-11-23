import os
import requests
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

TELEGRAM_TOKEN = os.getenv("8522657243:AAHI9WqZjTFJqj8Hr4XcSAkEyCc8LGVgGHY")
CHAT_ID = os.getenv("490304334")
MARKET_ID = os.getenv("1763889225444")
PRICE_THRESHOLD = float(os.getenv("PRICE_THRESHOLD", 0.70))

bot = Bot(token=TELEGRAM_TOKEN)

def get_polymarket_price(market_id):
    url = f"https://clob.polymarket.com/book/{market_id}"
    data = requests.get(url).json()

    best_yes = float(data["yes"]["bids"][0]["price"]) / 1e6
    return best_yes

def check_market():
    price = get_polymarket_price(MARKET_ID)
    print("Prix actuel :", price)

    if price > PRICE_THRESHOLD:
        bot.send_message(
            chat_id=CHAT_ID,
            text=f"🔥 ALERTE ! Le prix du marché {MARKET_ID} est à {price:.2f}"
        )

scheduler = BlockingScheduler()
scheduler.add_job(check_market, 'interval', seconds=30)

print("Bot lancé…")
scheduler.start()
