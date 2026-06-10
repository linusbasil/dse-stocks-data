import json
import os
from datetime import datetime, timezone
import yfinance as yf

# List of DSE tickers (add more as needed)
# Note: yfinance supports some DSE tickers with .TZ suffix
TICKERS = [
    "CRDB.TZ",   # CRDB Bank
    "DCB.TZ",    # DCB Bank
    "NICO.TZ",   # NICOL
    "TCC.TZ",    # Tanzania Cigarette Company
    "SWALA.TZ",  # Swala
    "TPCC.TZ",   # TPCC
    "VODA.TZ",   # Vodacom Tanzania
]

def fetch_stock_data():
    stocks = []
    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get('regularMarketPrice', info.get('currentPrice', 0))
            prev_close = info.get('regularMarketPreviousClose', 0)
            change_percent = ((price - prev_close) / prev_close * 100) if prev_close else 0.0
            
            stocks.append({
                "ticker": ticker.replace(".TZ", ""),
                "name": info.get('longName', ticker),
                "price": round(price, 2),
                "changePercent": round(change_percent, 2),
                "volumeNote": "normal"
            })
            print(f"OK {ticker} {price}")
        except Exception as e:
            print(f"FAIL {ticker}: {e}")
    return stocks

def main():
    stocks = fetch_stock_data()
    
    # Create output data
    output = {
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        "stocks": stocks,
        "topMover": max(stocks, key=lambda x: abs(x["changePercent"])) if stocks else None,
        "freshnessBadge": {
            "status": "current",
            "hoursSinceUpdate": 0
        }
    }
    
    # Write to public folder
    os.makedirs("public", exist_ok=True)
    with open("public/market-data.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("✅ market-data.json written successfully")

if __name__ == "__main__":
    main()
