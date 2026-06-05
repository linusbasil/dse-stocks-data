import json
import csv
from datetime import datetime

prices = {
    "CRDB": 2940, "NMB": 13800, "VODA": 800, "TBL": 10200,
    "TPCC": 7400, "DCB": 750, "DSE": 1050, "KCB": 510
}

data = {
    "date": datetime.now().date().isoformat(),
    "prices": prices
}

with open("dse_prices.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ dse_prices.json created successfully!")
print(json.dumps(data, indent=2))
