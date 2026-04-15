from pathlib import Path
import time
import pandas as pd
import yfinance as yf

tickers = ["JPM", "BAC", "C", "WFC", "GS", "MS"]

all_rows = []

for ticker_symbol in tickers:
    try:
        print(f"Extrayendo holders para {ticker_symbol}...")

        ticker = yf.Ticker(ticker_symbol)

        # Algunos tickers tienen institutional_holders
        holders = ticker.institutional_holders

        if holders is None or holders.empty:
            print(f"{ticker_symbol}: no tiene holders disponibles")
            continue

        holders = holders.copy()

        # Normalizar nombres de columnas si existen
        holders["ticker"] = ticker_symbol

        # Crear columnas estándar pedidas por la prueba
        holders["date"] = pd.Timestamp.today().normalize()
        holders["holder"] = holders["Holder"] if "Holder" in holders.columns else None
        holders["shares"] = holders["Shares"] if "Shares" in holders.columns else None
        holders["value"] = holders["Value"] if "Value" in holders.columns else None

        final_df = holders[["ticker", "date", "holder", "shares", "value"]]

        all_rows.append(final_df)

        print(f"{ticker_symbol}: {len(final_df)} holders extraídos")

        time.sleep(2)

    except Exception as e:
        print(f"Error con {ticker_symbol}: {e}")

if all_rows:
    result = pd.concat(all_rows, ignore_index=True)
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "all_banks_holders.csv"

    result.to_csv(output_file, index=False)

    print(f"File generated successfully: {output_file}")
    print(result.head())
else:
    print("No se pudo extraer información de holders.")