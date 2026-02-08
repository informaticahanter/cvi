import streamlit as st
import requests

# Configuración de Cloudflare (Usa st.secrets para seguridad)
CF_ACCOUNT_ID = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
CF_DATABASE_ID = st.secrets["CLOUDFLARE_DATABASE_ID"]
CF_API_TOKEN = st.secrets["CLOUDFLARE_API_TOKEN"]

def query_d1(sql, params=None):
    """Ejecuta una consulta SQL en Cloudflare D1 vía API."""
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_DATABASE_ID}/query"
    
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "sql": sql,
        "params": params if params else []
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if result.get("success"):
        # D1 devuelve una lista de resultados por cada query
        return result["result"][0]["results"]
    else:
        st.error(f"Error en D1: {result['errors'][0]['message']}")
        return None