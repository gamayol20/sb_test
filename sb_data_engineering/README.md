# Prueba Técnica de Ingeniería de Datos – Superintendencia de Bancos

## Objetivo

Construir un pipeline de datos end-to-end para extraer, validar, transformar y disponibilizar información financiera de bancos que cotizan en la bolsa de valores de los Estados Unidos, utilizando Yahoo Finance como fuente de datos.

## Arquitectura

La solución fue implementada bajo un enfoque por capas para separar la extracción, almacenamiento, transformación, validación y explotación analítica de los datos.

- **Fuente de datos:** Yahoo Finance
- **Extracción:** Scripts Python utilizando la librería `yfinance`
- **Landing Zone:** PostgreSQL para almacenamiento de datos crudos
- **Capa OLAP:** ClickHouse para explotación analítica
- **Transformación y calidad:** DBT para modelado, validaciones y pruebas de calidad
- **Orquestación:** Airflow
- **Despliegue:** Docker Compose

## Decisión de integración de datos

Aunque el enunciado recomienda el uso de Airbyte, en esta solución se implementó un mecanismo de integración personalizado utilizando scripts Python, almacenamiento intermedio en archivos CSV y orquestación mediante Apache Airflow, manteniendo un flujo end-to-end completamente automatizado y controlado.

## Estructura del Proyecto

sb_data_engineering/
├── airflow/
│   └── dags/
├── app/
│   ├── extract/
│   ├── load/
│   ├── tests/
│   └── utils/
├── data/
│   ├── raw/
│   └── samples/
├── dbt/
│   └── sb_finance_project/
├── docs/
│   └── arquitectura/
│   └── screenshots/
├── sql/
├── docker-compose.yml
├── airflow-requirements.txt
├── requirements.txt
└── README.md


## Flujo del Pipeline

1. Se extraen los datos desde Yahoo Finance mediante scripts en Python.
2. Los archivos generados se almacenan en la carpeta `data/raw`.
3. Los datos son cargados en PostgreSQL como capa de landing.
4. Posteriormente, los datos son llevados a ClickHouse como capa analítica.
5. Sobre ClickHouse se ejecutan modelos y pruebas en DBT.
6. Se construye una tabla de resumen mensual con métricas agregadas.

## Se extrajeron los siguientes conjuntos de datos para bancos listados en la bolsa de valores de los Estados Unidos:

## Información básica
- Industry
- Sector
- Employee Count
- City
- Phone
- State
- Country
- Website
- Address

## Precios diarios

Date
Open
High
Low
Close
Volume

## Fundamentales

Assets
Debt
Invested Capital
Share Issued

## Tenedores

Date
Holder
Shares
Value

Calificadores

Date
To Grade
From Grade
Action
Tablas de Landing

## Las tablas creadas en PostgreSQL para la zona de aterrizaje fueron:

raw_informacion_basica
raw_precios_diarios
raw_fundamentales
raw_tenedores
raw_calificadores
Tablas OLAP

## Las tablas creadas en ClickHouse para la capa analítica fueron:

dim_bank_info
fact_daily_prices
fact_fundamentals
fact_holders
fact_ratings
monthly_stock_summary
Reglas de Calidad de Datos

## Se implementaron pruebas de calidad con DBT sobre el modelo stg_fact_daily_prices, validando que los siguientes campos no contengan valores nulos:

ticker
trade_date
open_price
high_price
low_price
close_price
volume

## Cómo ejecutar el proyecto

1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd sb_data_engineering

2. Crear entorno virtual
python -m venv .venv

3. Instalar dependencias
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

4. Levantar contenedores
docker compose up -d

5. Ejecutar scripts de extracción
.\.venv\Scripts\python.exe .\app\extract\extract_basic_info_multi.py
.\.venv\Scripts\python.exe .\app\extract\extract_prices_multi.py
.\.venv\Scripts\python.exe .\app\extract\extract_fundamentals_multi.py
.\.venv\Scripts\python.exe .\app\extract\extract_holders_multi.py
.\.venv\Scripts\python.exe .\app\extract\extract_ratings_multi.py

6. Cargar landing zone en PostgreSQL
.\.venv\Scripts\python.exe .\app\load\load_landing_postgres.py

7. Cargar capa analítica en ClickHouse
.\.venv\Scripts\python.exe .\app\load\load_clickhouse.py

8. Ejecutar DBT
dbt debug
dbt run
dbt test


## Capturas de Pantalla

Las evidencias incluyen:

- Ejecución de contenedores en Docker
- Carga de datos en PostgreSQL
- Validación de tablas raw
- Carga de datos en ClickHouse
- Ejecución de dbt debug
- Ejecución de dbt run
- Ejecución de dbt test
- Resultados de monthly_stock_summary
- Ejecución del DAG en Airflow

## Resultados

Como resultado final se generó una tabla de resumen mensual con:

- Promedio mensual del precio de apertura
- Promedio mensual del precio de cierre
- Promedio mensual del volumen transado

## Consideraciones Técnicas

- Se utilizó PostgreSQL como landing zone para aislar los datos crudos.
- ClickHouse fue seleccionado como motor OLAP por su eficiencia en consultas analíticas.
- DBT permitió implementar validaciones de calidad y modelado desacoplado.
- Airflow se utilizó para orquestar el pipeline completo.
- La solución fue completamente contenerizada usando Docker Compose para garantizar portabilidad.