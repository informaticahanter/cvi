import streamlit as st
import pandas as pd
from modules.database import query_d1 

def login_screen():
    """Interfaz principal de acceso al sistema ALTO ERP"""
    
    st.markdown("<h1 style='text-align: center;'>🛡️ ORB ERP</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Sistema de Gestión de Inventario</p>", unsafe_allow_html=True)
    
    # Pestañas simplificadas
    tab_login, tab_registro = st.tabs(["🔐 Iniciar Sesión", "🚀 Registrar Empresa"])

    with tab_login:
        render_login()

    with tab_registro:
        from modules import registro_empresa
        registro_empresa.render_registro()

def render_login():
    """Formulario y lógica de inicio de sesión conectada a Cloudflare D1"""
    with st.container(border=True):
        st.write("### Credenciales de Acceso")
        
        empresa_nom = st.text_input(
            "Nombre de la Empresa", 
            placeholder="Ej: Hanter Metals", 
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
                    # SQL Simplificado: Eliminamos joins innecesarios
                    sql = """
                        SELECT u.id, u.username, u.nombre_real, u.rol, u.empresa_id, e.nombre as empresa_nombre 
                        FROM usuarios u
                        JOIN empresas e ON u.empresa_id = e.id
                        WHERE e.nombre = ? AND u.username = ? AND u.password = ?
                    """
                    
                    res_list = query_d1(sql, [empresa_nom, username, password])

                    if res_list and len(res_list) > 0:
                        user_data = res_list[0]
                        
                        # Guardamos en session_state (Sin departamentos)
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_data['id']
                        st.session_state.user = user_data['username']
                        st.session_state.nombre_real = user_data['nombre_real']
                        st.session_state.empresa_id = int(user_data['empresa_id'])
                        st.session_state.empresa_nombre = user_data['empresa_nombre']
                        st.session_state.rol = user_data['rol']
                        
                        st.success(f"Bienvenido, {st.session_state.nombre_real}")
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas o empresa no registrada.")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
            else:
                st.warning("Por favor, complete todos los campos.")

def logout():
    """Limpia la sesión y redirige al login"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()