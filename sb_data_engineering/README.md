# Prueba Técnica de Ingeniería de Datos – SB

## Objetivo

Construir un pipeline de datos end-to-end para extraer, validar, transformar y disponibilizar información financiera de bancos que cotizan en la bolsa de valores de los Estados Unidos, utilizando Yahoo Finance como fuente de datos.

---

## Arquitectura

La solución fue implementada bajo un enfoque por capas para separar la extracción, almacenamiento, transformación, validación y explotación analítica de los datos.

- **Fuente de datos:** Yahoo Finance  
- **Extracción:** Scripts en Python utilizando la librería `yfinance`  
- **Landing Zone:** PostgreSQL para almacenamiento de datos crudos  
- **Capa OLAP:** ClickHouse para explotación analítica  
- **Transformación y calidad:** DBT para modelado, validaciones y pruebas de calidad  
- **Orquestación:** Apache Airflow  
- **Despliegue:** Docker Compose  

---

## Decisión de integración de datos

Aunque el enunciado recomienda el uso de Airbyte, en esta solución se implementó un mecanismo de integración personalizado utilizando:

- Scripts Python  
- Archivos CSV como capa intermedia  
- Orquestación con Airflow  

Esto permitió mantener un flujo completamente automatizado y controlado, cumpliendo con los requerimientos funcionales del pipeline.

---

## Estructura del Proyecto

```text
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
│   ├── arquitectura/
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

- Date
- Open
- High
- Low
- Close
- Volume

## Fundamentales

- Assets
- Debt
- Invested Capital
- Share Issued

## Tenedores

- Date
- Holder
- Shares
- Value

## Calificadores

- Date
- To Grade
- From Grade
- Action

## Tablas de Landing (PostgreSQL):

- raw_informacion_basica
- raw_precios_diarios
- raw_fundamentales
- raw_tenedores
- raw_calificadores

## Tablas OLAP (ClickHouse):

- dim_bank_info
- fact_daily_prices
- fact_fundamentals
- fact_holders
- fact_ratings
- monthly_stock_summary

## Reglas de Calidad de Datos
Se implementaron pruebas de calidad con DBT sobre el modelo stg_fact_daily_prices, validando que los siguientes campos no contengan valores nulos:

- ticker
- trade_date
- open_price
- high_price
- low_price
- close_price
- volume

## Cómo ejecutar el proyecto

1. Clonar el repositorio
git clone <https://github.com/gamayol20/sb_test.git>
cd sb_data_engineering

2. Levantar contenedores
docker compose up -d

Esto levantará los siguientes servicios:

- PostgreSQL (Landing Zone)
- ClickHouse (OLAP)
- Airflow Webserver
- Airflow Scheduler

3. Acceder a Airflow

Abrir en el navegador:

http://localhost:8080

Credenciales:

- Usuario: admin
- Contraseña: admin

4. Ejecutar el pipeline

Dentro de Airflow:

Activar el DAG sb_finance_pipeline
Ejecutar manualmente el DAG

El pipeline ejecuta automáticamente:

- Extracción de datos desde Yahoo Finance
- Almacenamiento en archivos CSV (data/raw)
- Carga de datos en PostgreSQL (landing zone)
- Integración de datos hacia ClickHouse (capa analítica)

5. Validación de carga incremental

Antes de cargar los datos hacia ClickHouse, el proceso valida si existen nuevos registros en la landing zone (PostgreSQL) mediante una tabla de control (etl_control).

Si no se detectan cambios en los datos, la carga hacia ClickHouse se omite, optimizando el proceso.

6. Ejecución de transformaciones y calidad de datos con DBT

Las validaciones y transformaciones se ejecutan de forma independiente desde el proyecto DBT.

- Ubicarse en la carpeta del proyecto:

cd dbt/sb_finance_project

Ejecutar:

dbt debug
dbt run
dbt test

## Ejecución manual (opcional)

Para fines de prueba o depuración, los scripts también pueden ejecutarse manualmente:

1. Clonar el repositorio
git clone <https://github.com/gamayol20/sb_test.git>
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
cd dbt/sb_finance_project
dbt debug
dbt run
dbt test


## Capturas de Pantalla

Las evidencias del funcionamiento se encuentran en docs/screenshots/, incluyendo:

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

Se construyó un pipeline funcional que permite:

- Integración de múltiples fuentes de datos
- Validación de calidad automatizada
- Explotación analítica eficiente

## Resultado final

Tabla monthly_stock_summary con:

- Promedio mensual del precio de apertura
- Promedio mensual del precio de cierre
- Promedio mensual del volumen transado

## Consideraciones Técnicas

- PostgreSQL se utilizó como landing zone para aislar datos crudos
- ClickHouse se seleccionó como motor OLAP por su alto rendimiento
- DBT permitió desacoplar lógica de transformación y calidad
- Airflow permitió automatizar el pipeline completo
- Docker Compose garantiza portabilidad y reproducibilidad