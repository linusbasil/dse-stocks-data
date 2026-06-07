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
        print("Tables found: " + str(len(tables)))

        for i, table in enumerate(tables):
            rows = table.find_all("tr")
            print("Table " + str(i) + " has " + str(len(rows)) + " rows")
            for row in rows[:3]:
                cols = row.find_all("td")
                print("Row cols: " + str(len(cols)))
                for j, col in enumerate(cols):
                    print("  Col " + str(j) + ": " + col.text.strip()[:50])
                    link = col.find("a")
                    if link:
                        print("  Link href: " + str(link.get("href","")))

    except Exception as e:
        print("Error: " + str(e))
    return prices

prices = fetch_dse_prices()
print("Done")
