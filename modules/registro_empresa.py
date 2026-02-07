import streamlit as st
import sqlite3

def render_registro():
    st.subheader("🚀 Registro de Nueva Empresa")
    
    with st.container(border=True):
        # Añadimos parámetros 'key' únicos para evitar errores de Duplicados
        nombre_empresa = st.text_input(
            "Nombre de la Empresa", 
            placeholder="Ej: Logística Global S.A.",
            key="reg_nombre_empresa"
        )
        
        nombre_admin = st.text_input(
            "Nombre del Super Administrador", 
            placeholder="Nombre completo",
            key="reg_nombre_admin"
        )
        
        user_admin = st.text_input(
            "Usuario Administrador", 
            placeholder="admin_empresa",
            key="reg_user_admin"
        )
        
        pass_admin = st.text_input(
            "Contraseña", 
            type="password",
            key="reg_pass_admin"
        )
        
        confirm_pass = st.text_input(
            "Confirmar Contraseña", 
            type="password",
            key="reg_confirm_pass"
        )

        if st.button("Crear Empresa", use_container_width=True):
            if not (nombre_empresa and user_admin and pass_admin):
                st.error("Todos los campos son obligatorios.")
            elif pass_admin != confirm_pass:
                st.error("Las contraseñas no coinciden.")
            else:
                try:
                    conn = sqlite3.connect('inventario.db')
                    cursor = conn.cursor()
                    
                    # 1. Insertar Empresa
                    cursor.execute("INSERT INTO empresas (nombre) VALUES (?)", (nombre_empresa,))
                    empresa_id = cursor.lastrowid
                    
                    # 2. Insertar Usuario con rol SuperAdmin
                    # Nota: Mantenemos el campo 'rol' para la jerarquía que solicitaste
                    cursor.execute("""
                        INSERT INTO usuarios (username, password, empresa_id, rol, nombre_real) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (user_admin, pass_admin, empresa_id, 'SuperAdmin', nombre_admin))
                    
                    conn.commit()
                    conn.close()
                    st.success(f"¡Empresa {nombre_empresa} registrada con éxito! Ya puedes iniciar sesión.")
                    
                except sqlite3.IntegrityError:
                    st.error("El nombre de empresa o usuario ya existe.")
                except Exception as e:
                    st.error(f"Error al registrar: {e}")