-- ==========================================================
-- SCRIPT DE TABLAS PARA CLOUDFLARE D1 - ORBERP
-- ==========================================================

-- 1. Tabla de Categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    empresa_id INTEGER NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

-- 2. Tabla de Productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    sku TEXT, 
    precio_compra REAL DEFAULT 0,
    precio_venta REAL DEFAULT 0,
    stock INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 0,
    categoria_id INTEGER,
    empresa_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id),
    UNIQUE(sku, empresa_id) -- Un SKU no se puede repetir en la misma empresa
);

-- 3. Tabla de Movimientos
CREATE TABLE IF NOT EXISTS movimientos_inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    tipo TEXT CHECK(tipo IN ('Entrada', 'Salida')),
    cantidad INTEGER NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TI

    -- 1. Tabla de Ventas (Encabezado)
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    total REAL DEFAULT 0.0,
    usuario_id INTEGER NOT NULL,
    empresa_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

-- 2. Detalle de Venta
CREATE TABLE IF NOT EXISTS detalle_venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- 1. Tabla de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    dni_ruc TEXT,
    telefono TEXT,
    empresa_id INTEGER NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

-- 2. Agregar columna cliente_id a la tabla de ventas 
-- (Si la tabla ya existe, usa este comando)
ALTER TABLE ventas ADD COLUMN cliente_id INTEGER REFERENCES clientes(id);