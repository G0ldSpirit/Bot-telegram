import os
import time
import requests

TELEGRAM_TOKEN = os.getenv("8522657243:AAHI9WqZjTFJqj8Hr4XcSAkEyCc8LGVgGHY")
CHAT_ID = os.getenv("490304334")

# Slug de ton event Polymarket
SLUG = "highest-temperature-in-london-on-november-23"

THRESHOLD = 0.65  # 65%

def get_markets(slug):
    """Récupère tous les markets liés à l'événement."""
    url = f"https://gamma-api.polymarket.com/public-search?q={slug}"
    r = requests.get(url)
    data = r.json()

    markets = []

    if "events" in data:
        for ev in data["events"]:
            if ev.get("slug") == slug:
                for m in ev.get("markets", []):
                    markets.append({
                        "id": m["id"],
                        "question": m.get("question", "Marché sans nom")
                    })
    return markets

def get_price(market_id):
    """Récupère la probabilité YES pour un marché."""
    url = f"https://clob.polymarket.com/markets/{market_id}"
    r = requests.get(url)
    data = r.json()

    yes_price = data["outcomes"][0]["price"]
    return yes_price

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def main():
    send_telegram_message("🚀 Bot lancé ! Alerte dès qu’un marché dépasse 65%")

    markets = get_markets(SLUG)

    if not markets:
        send_telegram_message("❌ Aucun marché trouvé pour ce slug.")
        return

    send_telegram_message(f"🔍 {len(markets)} marchés détectés sur cet event.")

    while True:
        try:
            for m in markets:
                price = get_price(m["id"])
                print(f"{m['question']} : {price}")

                if price >= THRESHOLD:
                    send_telegram_message(
                        f"🔥 *ALERTE* !\n"
                        f"📈 Marché : *{m['question']}*\n"
                        f"➡️ Probabilité actuelle : *{price*100:.1f}%*\n"
                        f"🔺 Seuil dépassé (>{THRESHOLD*100:.0f}%)"
                    )
                    time.sleep(300)  # 5 minutes pour éviter spam

        except Exception as e:
            print("Erreur :", e)

        time.sleep(30)

if __name__ == "__main__":
    main()
