CREATE TABLE IF NOT EXISTS raw_informacion_basica (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20),
    nombre_empresa VARCHAR(255),
    industria VARCHAR(255),
    sector VARCHAR(255),
    cantidad_empleados BIGINT,
    ciudad VARCHAR(100),
    telefono VARCHAR(100),
    estado VARCHAR(100),
    pais VARCHAR(100),
    sitio_web VARCHAR(255),
    direccion VARCHAR(255),
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_precios_diarios (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20),
    fecha TIMESTAMP,
    precio_apertura NUMERIC(18,6),
    precio_maximo NUMERIC(18,6),
    precio_minimo NUMERIC(18,6),
    precio_cierre NUMERIC(18,6),
    volumen BIGINT,
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_fundamentales (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20),
    nombre_empresa VARCHAR(255),
    activos NUMERIC(20,2),
    deuda NUMERIC(20,2),
    capital_invertido NUMERIC(20,2),
    acciones_emitidas BIGINT,
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_tenedores (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20),
    fecha DATE,
    tenedor VARCHAR(255),
    acciones BIGINT,
    valor NUMERIC(20,2),
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_calificadores (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20),
    fecha DATE,
    calificacion_destino VARCHAR(100),
    calificacion_origen VARCHAR(100),
    accion VARCHAR(100),
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);