from pathlib import Path
import time
import pandas as pd
import yfinance as yf

REQUEST_DELAY_SECONDS = 2
ERROR_DELAY_SECONDS = 3

tickers = ["JPM", "BAC", "C", "WFC", "GS", "MS"]

all_rows = []

for ticker_symbol in tickers:
    try:
        print(f"Extrayendo ratings para {ticker_symbol}...")

        ticker = yf.Ticker(ticker_symbol)
        recs = ticker.recommendations

        if recs is None or recs.empty:
            print(f"{ticker_symbol}: no tiene ratings disponibles")
            continue

        recs = recs.copy().reset_index()

        # Normalización de columnas
        recs["ticker"] = ticker_symbol

        # Ajuste de nombres según lo que devuelve yfinance
        recs["date"] = recs["Date"] if "Date" in recs.columns else pd.Timestamp.today().normalize()
        recs["to_grade"] = recs["To Grade"] if "To Grade" in recs.columns else None
        recs["from_grade"] = recs["From Grade"] if "From Grade" in recs.columns else None
        recs["action"] = recs["Action"] if "Action" in recs.columns else None

        final_df = recs[["ticker", "date", "to_grade", "from_grade", "action"]]

        all_rows.append(final_df)

        print(f"{ticker_symbol}: {len(final_df)} ratings extraídos")

        time.sleep(REQUEST_DELAY_SECONDS)

    except Exception as e:
        print(f"Error con {ticker_symbol}: {e}")
        time.sleep(ERROR_DELAY_SECONDS)
        
if all_rows:
    result = pd.concat(all_rows, ignore_index=True)
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "all_banks_ratings.csv"

    result.to_csv(output_file, index=False)

    print(f"File generated successfully: {output_file}")
    print(result.head())
else:
    print("No se pudo extraer información de ratings.")