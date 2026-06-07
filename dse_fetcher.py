import requests
import urllib3
from bs4 import BeautifulSoup
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_dse_prices():
    url = "https://www.african-markets.com/en/stock-markets/dse/listed-companies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    prices = {}

    try:
        response = requests.get(url, headers=headers, timeout=20, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all table rows
        rows = soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                symbol = cols[0].text.strip()
                price = cols[2].text.strip()
                if symbol and price:
                    # Clean price (remove commas, spaces)
                    price_clean = price.replace(",", "").replace(" ", "")
                    prices[symbol] = price_clean
                    print(f"✅ {symbol}: {price_clean}")

    except Exception as e:
        print(f"❌ Error: {e}")

    return prices

prices = fetch_dse_prices()

if prices:
    with open("dse_prices.json", "w") as f:
        json.dump(prices, f, indent=2)
    print(f"\n✅ Saved {len(prices)} prices to dse_prices.json")
else:
    print("❌ No prices found")
