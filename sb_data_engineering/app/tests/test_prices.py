from pathlib import Path
import yfinance as yf

ticker_symbol = "JPM"
ticker = yf.Ticker(ticker_symbol)

df = ticker.history(start="2024-01-01", end="2025-12-31")
df.reset_index(inplace=True)

df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
df["ticker"] = ticker_symbol

output_dir = Path("data/samples")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "jpm_daily_prices.csv"
df.to_csv(output_file, index=False)

print(f"File generated successfully: {output_file}")
print(df.head())
print(df.tail())