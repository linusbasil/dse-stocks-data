import json
import yfinance as yf
from datetime import datetime

# All DSE symbols with correct Yahoo Finance suffix .TZ
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

def main():
    prices = {}
    for friendly, yahoo_symbol in SYMBOLS.items():
        ticker = yf.Ticker(yahoo_symbol)
        try:
            # Get current price (regular market price or previous close)
            info = ticker.info
            price = info.get('regularMarketPrice') or info.get('previousClose')
            if price:
                prices[friendly] = round(price, 2)
                print(f"✅ {friendly} ({yahoo_symbol}): {price}")
            else:
                print(f"⚠️ {friendly}: No price available")
        except Exception as e:
            print(f"❌ {friendly}: {e}")

    if not prices:
        print("❌ No prices fetched – keeping existing dse_prices.json")
        return

    data = {
        "date": datetime.now().date().isoformat(),
        "prices": prices
    }

    with open("dse_prices.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n✅ Updated dse_prices.json with {len(prices)} live prices")

if __name__ == "__main__":
    main()
