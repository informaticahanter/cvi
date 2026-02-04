import sqlite3

def inicializar_sistema():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # 1. Maestro de Empresas
    cursor.execute('''CREATE TABLE IF NOT EXISTS empresas 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)''')

    # 2. Usuarios: Amarrados a la empresa
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, 
         empresa_id INTEGER, 
         FOREIGN KEY(empresa_id) REFERENCES empresas(id))''')

    # 3. Productos: Amarrados a la empresa
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, stock INTEGER, precio REAL, 
         empresa_id INTEGER, 
         FOREIGN KEY(empresa_id) REFERENCES empresas(id))''')

    # 4. Movimientos (Compras/Ventas): El registro histórico amarrado a la empresa
    cursor.execute('''CREATE TABLE IF NOT EXISTS movimientos 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER, tipo TEXT, 
         cantidad INTEGER, precio_unitario REAL, fecha DATETIME DEFAULT CURRENT_TIMESTAMP, 
         empresa_id INTEGER,
         FOREIGN KEY(producto_id) REFERENCES productos(id),
         FOREIGN KEY(empresa_id) REFERENCES empresas(id))''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_sistema()