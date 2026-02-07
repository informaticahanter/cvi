import streamlit as st
import pandas as pd
import sqlite3

def get_connection():
    return sqlite3.connect('inventario.db')

def render_dashboard():
    st.header("📊 Panel de Control")
    empresa_id = st.session_state.empresa_id
    
    # Lógica de consulta aislada por empresa
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM productos WHERE empresa_id=?", conn, params=(empresa_id,))
    conn.close()
    
    if not df.empty:
        c1, c2 = st.columns(2)
        c1.metric("Total SKU", len(df))
        c2.metric("Valor Inventario", f"${(df['stock']*df['precio']).sum():,.2f}")
    else:
        st.info("No hay datos disponibles.")

def render_table():
    st.subheader("📦 Listado de Existencias")
    # Aquí iría el st.dataframe con st.column_config que diseñamos
    pass