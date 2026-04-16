import time
import pandas as pd
import yfinance as yf
from pathlib import Path

REQUEST_DELAY_SECONDS = 2
ERROR_DELAY_SECONDS = 3

tickers = ["JPM", "BAC", "C", "WFC", "GS", "MS"]

rows = []

for ticker_symbol in tickers:
    try:
        print(f"Extrayendo información básica para {ticker_symbol}...")

        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        row = {
            "ticker": ticker_symbol,
            "company_name": info.get("longName"),
            "industry": info.get("industry"),
            "sector": info.get("sector"),
            "employee_count": info.get("fullTimeEmployees"),
            "city": info.get("city"),
            "phone": info.get("phone"),
            "state": info.get("state"),
            "country": info.get("country"),
            "website": info.get("website"),
            "address": info.get("address1"),
        }

        rows.append(row)
        print(f"{ticker_symbol}: información extraída correctamente")

        time.sleep(REQUEST_DELAY_SECONDS)

    except Exception as e:
        print(f"Error con {ticker_symbol}: {e}")
        time.sleep(ERROR_DELAY_SECONDS)

df = pd.DataFrame(rows)

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "all_banks_basic_info.csv"

df.to_csv(output_file, index=False)

print(f"File generated successfully: {output_file}")
print(df.head())