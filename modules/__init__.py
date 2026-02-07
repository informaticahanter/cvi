import sqlite3

def init_db():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Tabla de Empresas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    ''')

    # Tabla de Usuarios (CORREGIDA con rol y nombre_real)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            empresa_id INTEGER,
            rol TEXT,
            nombre_real TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id)
        )
    ''')

    # Tabla de Productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            stock INTEGER DEFAULT 0,
            precio REAL DEFAULT 0.0,
            empresa_id INTEGER,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de datos recreada con éxito.")

if __name__ == "__main__":
    init_db()