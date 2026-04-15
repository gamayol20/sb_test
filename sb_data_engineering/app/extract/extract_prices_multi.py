from pathlib import Path
import time
import pandas as pd
import yfinance as yf

tickers = ["JPM", "BAC", "C", "WFC", "GS", "MS"]

all_data = []

for ticker_symbol in tickers:
    try:
        print(f"Extrayendo precios para {ticker_symbol}...")

        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start="2024-01-01", end="2025-12-31")

        if df.empty:
            print(f"No se encontraron datos para {ticker_symbol}")
            continue

        df = df.reset_index()
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df["ticker"] = ticker_symbol

        all_data.append(df)

        print(f"{ticker_symbol}: {len(df)} filas extraídas")

        time.sleep(2)

    except Exception as e:
        print(f"Error con {ticker_symbol}: {e}")

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "all_banks_daily_prices.csv"

    final_df.to_csv(output_file, index=False)

    print(f"File generated successfully: {output_file}")
    print(final_df.head())
    print(final_df.tail())
else:
    print("No se pudo extraer información.")