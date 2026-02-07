import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # 1. Tabla de Empresas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    ''')

    # 2. Tabla de Departamentos (Para la jerarquía solicitada)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empresa_id INTEGER,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id)
        )
    ''')

    # 3. Tabla de Usuarios (Incluye rol y nombre_real)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            empresa_id INTEGER,
            departamento_id INTEGER,
            rol TEXT, -- SuperAdmin o Encargado
            nombre_real TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id),
            FOREIGN KEY (departamento_id) REFERENCES departamentos (id)
        )
    ''')

    # 4. Tabla de Productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            stock INTEGER DEFAULT 0,
            precio REAL DEFAULT 0.0,
            empresa_id INTEGER,
            departamento_id INTEGER,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id),
            FOREIGN KEY (departamento_id) REFERENCES departamentos (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de datos 'inventario.db' creada con la estructura correcta.")

if __name__ == "__main__":
    crear_base_datos()