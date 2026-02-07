import streamlit as st
import sqlite3
import pandas as pd
from modules import registro_empresa 

def get_connection():
    return sqlite3.connect('inventario.db')

def login_screen():
    """Interfaz principal de acceso al sistema"""
    
    st.markdown("<h1 style='text-align: center;'>🛡️ CVI System</h1>", unsafe_allow_html=True)
    
    # Pestañas para Login y Registro
    tab_login, tab_registro = st.tabs(["🔐 Iniciar Sesión", "🚀 Registrar Empresa"])

    with tab_login:
        render_login()

    with tab_registro:
        # Llamamos al documento externo ya modificado con sus propias keys
        registro_empresa.render_registro()

def render_login():
    """Formulario y lógica de inicio de sesión con Keys únicas"""
    with st.container(border=True):
        st.write("### Credenciales de Acceso")
        
        # Se añaden 'key' únicas para evitar el error StreamlitDuplicateElementId
        empresa_nom = st.text_input(
            "Nombre de la Empresa", 
            placeholder="Ej: Mi Negocio S.A.", 
            key="log_empresa_nom"
        )
        username = st.text_input(
            "Nombre de Usuario", 
            placeholder="admin", 
            key="log_username"
        )
        password = st.text_input(
            "Contraseña", 
            type="password", 
            key="log_password"
        )

        if st.button("Ingresar al Sistema", use_container_width=True, key="log_btn"):
            if empresa_nom and username and password:
                try:
                    conn = get_connection()
                    query = """
                        SELECT u.*, e.nombre as empresa_nombre 
                        FROM usuarios u
                        JOIN empresas e ON u.empresa_id = e.id
                        WHERE e.nombre = ? AND u.username = ? AND u.password = ?
                    """
                    res = pd.read_sql_query(query, conn, params=(empresa_nom, username, password))
                    conn.close()

                    if not res.empty:
                        # Extraemos los datos de la primera fila
                        user_data = res.iloc[0]
                        
                        # Guardamos en session_state
                        st.session_state.logged_in = True
                        st.session_state.user = user_data['username']
                        st.session_state.nombre_real = user_data['nombre_real']
                        st.session_state.empresa_id = int(user_data['empresa_id'])
                        st.session_state.empresa_nombre = user_data['empresa_nombre']
                        st.session_state.rol = user_data['rol']
                        
                        st.success(f"Bienvenido, {st.session_state.nombre_real}")
                        st.rerun()
                    else:
                        st.error("Datos incorrectos. Verifique el nombre de la empresa y sus credenciales.")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
            else:
                st.warning("Por favor, complete todos los campos.")

def logout():
    """Función para limpiar la sesión y salir"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()