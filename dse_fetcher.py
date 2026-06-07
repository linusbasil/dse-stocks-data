import json
import urllib.request
import time
from datetime import datetime
import os

# DSE symbols as Alpha Vantage expects (they use .TZ suffix)
SYMBOLS = {
    "CRDB": "CRDB.TZ",
    "NMB": "NMB.TZ",
    "VODA": "VODA.TZ",
    "TBL": "TBL.TZ",
    "TPCC": "TPCC.TZ",
    "DCB": "DCB.TZ",
    "DSE": "DSE.TZ",
    "KCB": "KCB.TZ",
    "TOL": "TOL.TZ",
    "TCC": "TCC.TZ",
    "SWISS": "SWISS.TZ",
    "NICO": "NICO.TZ",
    "MKCB": "MKCB.TZ",
    "EABL": "EABL.TZ",
    "JHL": "JHL.TZ",
    "MCC": "MCC.TZ",
    "NMG": "NMG.TZ",
    "NICOL": "NICOL.TZ",
    "PCC": "PCC.TZ",
    "TCCIA": "TCCIA.TZ",
    "TICL": "TICL.TZ",
    "TPC": "TPC.TZ",
    "TCCL": "TCCL.TZ"
}

API_KEY = os.environ.get("ALPHA_VANTAGE_KEY")

def fetch_alpha_vantage(yahoo_symbol):
    """Fetch price from Alpha Vantage using the symbol (Yahoo format)."""
    if not API_KEY:
        return None
    # Alpha Vantage uses same ticker format for global stocks
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={yahoo_symbol}&apikey={API_KEY}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            quote = data.get("Global Quote", {})
            price = quote.get("05. price")
            if price:
                return round(float(price), 2)
    except Exception as e:
        print(f"⚠️ Error fetching {yahoo_symbol}: {e}")
    return None

def main():
    if not API_KEY:
        print("❌ ALPHA_VANTAGE_KEY not set in secrets.")
        return

    prices = {}
    for friendly, yahoo in SYMBOLS.items():
        print(f"Fetching {friendly}...")
        price = fetch_alpha_vantage(yahoo)
        if price is not None:
            prices[friendly] = price
        else:
            print(f"⚠️ Could not fetch {friendly}")
        time.sleep(12)  # Alpha Vantage free tier: 5 calls per minute → 12 sec between calls

    if not prices:
        print("❌ No prices fetched – keeping existing dse_prices.json")
        return

    data = {
        "date": datetime.now().date().isoformat(),
        "prices": prices
    }

    with open("dse_prices.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ dse_prices.json updated with {len(prices)} live prices")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
