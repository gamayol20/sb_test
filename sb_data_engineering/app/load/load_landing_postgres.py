import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).resolve().parents[2]

USER = "postgres"
PASSWORD = "postgres"
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = "5432"
DATABASE = "gobierno_datos"

connection_string = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(connection_string)
files = [
    {
        "path": BASE_DIR / "data/raw/all_banks_basic_info.csv",
        "table": "raw_informacion_basica",
        "rename": {
            "company_name": "nombre_empresa",
            "industry": "industria",
            "sector": "sector",
            "employee_count": "cantidad_empleados",
            "city": "ciudad",
            "phone": "telefono",
            "state": "estado",
            "country": "pais",
            "website": "sitio_web",
            "address": "direccion",
        },
    },
    {
        "path": BASE_DIR / "data/raw/all_banks_daily_prices.csv",
        "table": "raw_precios_diarios",
        "rename": {
            "Date": "fecha",
            "Open": "precio_apertura",
            "High": "precio_maximo",
            "Low": "precio_minimo",
            "Close": "precio_cierre",
            "Volume": "volumen",
        },
    },
    {
        "path": BASE_DIR / "data/raw/all_banks_fundamentals.csv",
        "table": "raw_fundamentales",
        "rename": {
            "company_name": "nombre_empresa",
            "assets": "activos",
            "debt": "deuda",
            "invested_capital": "capital_invertido",
            "share_issued": "acciones_emitidas",
        },
    },
    {
        "path": BASE_DIR / "data/raw/all_banks_holders.csv",
        "table": "raw_tenedores",
        "rename": {
            "date": "fecha",
            "holder": "tenedor",
            "shares": "acciones",
            "value": "valor",
        },
    },
    {
        "path": BASE_DIR / "data/raw/all_banks_ratings.csv",
        "table": "raw_calificadores",
        "rename": {
            "date": "fecha",
            "to_grade": "calificacion_destino",
            "from_grade": "calificacion_origen",
            "action": "accion",
        },
    },
]

for file in files:
    try:
        print(f"Loading file: {file['path']}")

        df = pd.read_csv(file["path"])
        df = df.rename(columns=file["rename"])

        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", utc=True)

        if file["table"] == "raw_precios_diarios":
            df["fecha"] = df["fecha"].dt.tz_localize(None)

        if file["table"] in ["raw_tenedores", "raw_calificadores"]:
            df["fecha"] = df["fecha"].dt.date

        df.to_sql(file["table"], engine, if_exists="append", index=False)

        print(f"Data loaded successfully into table: {file['table']}")

    except FileNotFoundError:
        print(f"File not found: {file['path']}")
    except Exception as e:
        print(f"Error loading {file['path']}: {e}")