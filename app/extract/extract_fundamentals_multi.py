from pathlib import Path
import time
import pandas as pd
import yfinance as yf

REQUEST_DELAY_SECONDS = 2
ERROR_DELAY_SECONDS = 3

tickers = ["JPM", "BAC", "C", "WFC", "GS", "MS"]

rows = []

for ticker_symbol in tickers:
    try:
        print(f"Extrayendo fundamentales para {ticker_symbol}...")

        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        row = {
            "ticker": ticker_symbol,
            "company_name": info.get("longName"),
            "assets": info.get("totalAssets"),
            "debt": info.get("totalDebt"),
            "invested_capital": info.get("investedCapital"),
            "share_issued": info.get("sharesOutstanding"),
        }

        rows.append(row)
        print(f"{ticker_symbol}: fundamentales extraídos correctamente")

        time.sleep(REQUEST_DELAY_SECONDS)

    except Exception as e:
        print(f"Error con {ticker_symbol}: {e}")
        time.sleep(ERROR_DELAY_SECONDS)
        
    df = pd.DataFrame(rows)

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "all_banks_fundamentals.csv"

    df.to_csv(output_file, index=False)

    print(f"File generated successfully: {output_file}")
    print(df.head())