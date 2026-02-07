import streamlit as st
import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect('inventario.db')

def render_gestion_departamentos():
    st.header("🏢 Gestión de Departamentos")
    empresa_id = st.session_state.empresa_id

    # --- SECCIÓN 1: CREAR DEPARTAMENTO ---
    with st.expander("➕ Crear Nuevo Departamento", expanded=True):
        with st.form("form_dept"):
            nombre_dept = st.text_input("Nombre del Departamento", placeholder="Ej: Almacén Central")
            if st.form_submit_button("Registrar Departamento"):
                if nombre_dept:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO departamentos (nombre, empresa_id) VALUES (?, ?)", 
                                     (nombre_dept, empresa_id))
                        conn.commit()
                        conn.close()
                        st.success(f"Departamento '{nombre_dept}' creado.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Escriba un nombre.")

    # --- SECCIÓN 2: LISTADO Y ASIGNACIÓN ---
    st.subheader("📋 Departamentos Existentes")
    conn = get_connection()
    depts = pd.read_sql_query("SELECT * FROM departamentos WHERE empresa_id = ?", conn, params=(empresa_id,))
    conn.close()

    if not depts.empty:
        st.dataframe(depts[['id', 'nombre']], use_container_width=True, hide_index=True)
    else:
        st.info("Aún no hay departamentos creados.")

def render_gestion_usuarios():
    st.header("👥 Gestión de Usuarios y Jerarquías")
    empresa_id = st.session_state.empresa_id

    # Obtener departamentos para el selectbox
    conn = get_connection()
    depts = pd.read_sql_query("SELECT id, nombre FROM departamentos WHERE empresa_id = ?", conn, params=(empresa_id,))
    conn.close()

    with st.container(border=True):
        st.write("### Registrar Nuevo Usuario")
        u_nombre = st.text_input("Nombre Real", key="user_real")
        u_user = st.text_input("Nombre de Usuario", key="user_log")
        u_pass = st.text_input("Contraseña", type="password", key="user_pass")
        
        # Selección de Departamento y Rol (Jerarquía)
        col1, col2 = st.columns(2)
        with col1:
            # Los usuarios se agregan por departamento
            opciones_dept = {row['nombre']: row['id'] for _, row in depts.iterrows()}
            u_dept = st.selectbox("Asignar a Departamento", options=list(opciones_dept.keys()))
        with col2:
            # Jerarquía: Súper Administrador y Encargado
            u_rol = st.selectbox("Rol / Jerarquía", ["Encargado", "Súper Administrador"])

        if st.button("Crear Usuario", use_container_width=True):
            if u_nombre and u_user and u_pass:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    dept_id = opciones_dept[u_dept]
                    cursor.execute("""
                        INSERT INTO usuarios (username, password, empresa_id, departamento_id, rol, nombre_real)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (u_user, u_pass, empresa_id, dept_id, u_rol, u_nombre))
                    conn.commit()
                    conn.close()
                    st.success("Usuario creado exitosamente.")
                except Exception as e:
                    st.error(f"Error: {e}")