import requests
import json

# --- CONFIGURACIÓN MANUAL ---
CF_ACCOUNT_ID = "34c44d9d719d5977b5d87ac439c8a9bb"
CF_DATABASE_ID = "bdd5ca1c-4a91-4f66-9068-737fd78c8571"
CF_API_TOKEN = "d-4rBHRWFZeyBZrJU4NFcT0vbdbwmAivC6HZ6ZCv"

def query_d1_raw(sql):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"sql": sql, "params": []}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"success": False, "errors": [{"message": str(e)}]}

def crear_infraestructura_minima():
    # 1. Lista de todas las posibles tablas para limpiar la base de datos
    tablas_a_borrar = ["tareas", "productos", "usuarios", "departamentos", "empresas"]
    
    # 2. Definición de la estructura mínima esencial
    tablas_a_crear = [
        # Tabla de Empresas
        "CREATE TABLE empresas (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE NOT NULL)",
        
        # Tabla de Usuarios (Ligada solo a Empresa)
        "CREATE TABLE usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, empresa_id INTEGER, rol TEXT, nombre_real TEXT, FOREIGN KEY (empresa_id) REFERENCES empresas (id))",
        
        # Tabla de Productos (Inventario base)
        "CREATE TABLE productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, stock INTEGER DEFAULT 0, precio REAL DEFAULT 0.0, empresa_id INTEGER, FOREIGN KEY (empresa_id) REFERENCES empresas (id))"
    ]

    print("🛰️ Conectando con Cloudflare D1 (Modo Minimalista)...")

    # Limpieza total
    for tabla in tablas_a_borrar:
        query_d1_raw(f"DROP TABLE IF EXISTS {tabla}")
    print("🧹 Base de datos vaciada.")

    # Creación
    for sql in tablas_a_crear:
        res = query_d1_raw(sql)
        if res.get("success"):
            nombre_tabla = sql.split("TABLE ")[1].split(" (")[0]
            print(f"✅ Tabla '{nombre_tabla}' creada.")
        else:
            print(f"❌ Error: {res.get('errors')[0].get('message')}")

    print("\n✨ ALTO ERP: Estructura mínima lista.")

if __name__ == "__main__":
    crear_infraestructura_minima()