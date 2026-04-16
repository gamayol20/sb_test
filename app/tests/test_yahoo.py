import yfinance as yf

ticker = yf.Ticker("JPM")

info = ticker.info

print("Nombre:", info.get("longName"))
print("Sector:", info.get("sector"))
print("Industria:", info.get("industry"))
print("Ciudad:", info.get("city"))
print("País:", info.get("country"))
print("Website:", info.get("website"))