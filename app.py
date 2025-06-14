from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

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


@app.route("/")
def home():
    orders = get_red_mushroom_buy_orders()

    if orders is False:
        error = f"Failed to fetch data. HTTP Status: {response.status_code}"
        return render_template("index.html", error=error)
    elif orders is None:
        return render_template("index.html", error="Red Mushroom data not found.")
    else:
        return render_template("index.html", orders=orders)


if __name__ == "__main__":
    # Use the PORT environment variable provided by Render
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
