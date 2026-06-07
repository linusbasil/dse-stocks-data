import requests
from bs4 import BeautifulSoup
import json
import re
import os

SUPABASE_URL = "https://ghluqfrinjosvwxnggup.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

def fetch_dse_prices():
    url = "https://www.mansamarkets.com/tanzania"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    stocks = []
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        for table in tables:
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 3:
                    link = cols[1].find("a")
                    if link:
                        href = link.get("href", "")
                        ticker = href.split("/")[-1].upper()
                        symbol = ticker + " PLC"
                    else:
                        continue
                    price = re.sub(r'[^\d.]', '', cols[2].text.strip())
                    change = re.sub(r'[^\d.\-]', '', cols[3].text.strip()) if len(cols) > 3 else "0"
                    volume = re.sub(r'[^\d]', '', cols[4].text.strip()) if len(cols) > 4 else "0"
                    if symbol and price:
                        stocks.append({
                            "symbol": symbol,
                            "price": float(price) if price else 0,
                            "change_percent": float(change) if change else 0,
                            "volume": int(volume) if volume else 0,
                        })
                        print("Fetched " + symbol + ": " + price)
    except Exception as e:
        print("Fetch error: " + str(e))
    return stocks

def push_to_supabase(stocks):
    headers = {
        "apikey": SUPABASE_KEY,
        "
