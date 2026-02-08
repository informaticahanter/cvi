import streamlit as st
from modules.database import query_d1

@st.dialog("Notificación de Usuarios")
def mostrar_notificacion(titulo, detalle, es_error=False):
    if es_error:
        st.error(f"### ❌ Registro Inválido")
        st.write(f"**Motivo:** {detalle}")
    else:
        st.success(f"### ✅ {titulo}")
        st.write(detalle)
    if st.button("Entendido", use_container_width=True):
        st.rerun()

def render_usuarios():
    st.header("👥 Gestión de Usuarios - ORBERP")
    empresa_id = st.session_state.get('empresa_id')

    # --- FORMULARIO DE REGISTRO ---
    with st.expander("➕ Registrar Nuevo SuperAdmin", expanded=True):
        c1, c2, c3 = st.columns(3)
        nombre = c1.text_input("Nombre Real", placeholder="Ej: Juan Pérez")
        user = c2.text_input("Usuario (Login)", placeholder="jperez")
        pasw = c3.text_input("Contraseña", type="password")

        if st.button("🚀 Crear Acceso", use_container_width=True):
            if nombre and user and pasw:
                try:
                    sql = """INSERT INTO usuarios (username, password, nombre_real, rol, empresa_id) 
                             VALUES (?, ?, ?, 'SuperAdmin', ?)"""
                    query_d1(sql, [user, pasw, nombre, empresa_id])
                    mostrar_notificacion("Usuario Creado", f"El SuperAdmin {nombre} ha sido registrado.")
                except Exception as e:
                    if "UNIQUE constraint failed" in str(e):
                        mostrar_notificacion("Error", "Ese nombre de usuario ya está en uso.", es_error=True)
                    else:
                        mostrar_notificacion("Error", str(e), es_error=True)
            else:
                st.warning("Por favor, completa todos los campos.")

    st.divider()

    # --- LISTADO DE USUARIOS ---
    st.subheader("📋 Administradores del Sistema")
    
    sql_users = """
        SELECT nombre_real as 'Nombre', username as 'Usuario', 
               rol as 'Perfil'
        FROM usuarios 
        WHERE empresa_id = ?
    """
    
    try:
        lista_usuarios = query_d1(sql_users, [empresa_id])
        if lista_usuarios:
            st.dataframe(lista_usuarios, use_container_width=True, hide_index=True)
        else:
            st.info("No hay otros administradores registrados.")
    except Exception as e:
        st.error(f"Error al cargar usuarios: {e}")