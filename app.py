from flask import Flask, render_template
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)

cached_data = {
    "orders": None,
    "timestamp": None
}

CACHE_TTL = 30  # Reduced from 60 to 30 seconds

def get_red_mushroom_buy_orders():
    url = "https://api.hypixel.net/skyblock/bazaar" 
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        red_mushroom_key = "INK_SACK:3"

        if red_mushroom_key in data["products"]:
            red_mushroom = data["products"][red_mushroom_key]
            sorted_buy_orders = sorted(
                red_mushroom["buy_summary"],
                key=lambda x: x["pricePerUnit"],
                reverse=True
            )
            return sorted_buy_orders[:10]
        else:
            return None
    else:
        return False


def get_cached_red_mushroom_buy_orders():
    now = datetime.now()
    if (cached_data["orders"] is None or
        (now - cached_data["timestamp"]).seconds > CACHE_TTL):
        print("Fetching fresh data...")
        orders = get_red_mushroom_buy_orders()
        cached_data["orders"] = orders
        cached_data["timestamp"] = now
    else:
        print("Using cached data")
    return cached_data["orders"]


@app.route("/")
def home():
    orders = get_cached_red_mushroom_buy_orders()

    if orders is False:
        return render_template("index.html", error="Failed to fetch data.")
    elif orders is None:
        return render_template("index.html", error="Red Mushroom data not found.")
    else:
        return render_template("index.html", orders=orders)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
