import requests
from bs4 import BeautifulSoup
import json
import re

def fetch_dse_prices():
    url = "https://www.mansamarkets.com/tanzania"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    prices = {}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")

        for table in tables:
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 3:
                    # Ticker from link in Col 1
                    link = cols[1].find("a")
                    if link:
                        href = link.get("href", "")
                        ticker = href.split("/")[-1].upper()
                        symbol = ticker + " PLC"
                    else:
                        continue

                    # Price from Col 2
                    price_raw = cols[2].text.strip()
                    price = re.sub(r'[^\d.]', '', price_raw)

                    if symbol and price:
                        prices[symbol] = price
                        print("OK " + symbol + ": " + price)

    except Exception as e:
        print("Error: " + str(e))
    return prices

prices = fetch_dse_prices()
if prices:
    with open("dse_prices.json", "w") as f:
        json.dump(prices, f, indent=2)
    print("Saved " + str(len(prices)) + " prices")
else:
    print("No prices found")
