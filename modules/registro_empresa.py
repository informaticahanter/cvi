import streamlit as st
from modules.database import query_d1

@st.dialog("Notificación del Sistema")
def mostrar_notificacion(titulo, detalle, es_error=False):
    """
    Renderiza el mensaje estrictamente DENTRO del modal.
    - Si es error: Título 'Registro Inválido', color rojo, NO limpia componentes.
    """
    if es_error:
        # Forzamos el título solicitado y el color rojo
        st.error(f"### ❌ Registro Inválido")
        st.markdown(f"**Causa:** {detalle}")
        if st.button("Entendido", use_container_width=True, key="btn_modal_error"):
            # Al ser error, cerramos el modal sin st.rerun() global para mantener los datos
            st.rerun() 
    else:
        st.success(f"### ✅ {titulo}")
        st.write(detalle)
        if st.button("Entendido", use_container_width=True, key="btn_modal_success"):
            # Al ser éxito, st.rerun() limpia todos los inputs del formulario
            st.rerun()

def render_registro():
    st.subheader("🚀 Registro de Nueva Empresa")
    
    with st.container(border=True):
        nombre_empresa = st.text_input("Nombre de la Empresa", placeholder="Ej: Hanter Metals S.A.", key="reg_nombre_empresa")
        nombre_admin = st.text_input("Nombre del Super Administrador", placeholder="Nombre completo", key="reg_nombre_admin")
        user_admin = st.text_input("Usuario Administrador", placeholder="admin_empresa", key="reg_user_admin")
        pass_admin = st.text_input("Contraseña", type="password", key="reg_pass_admin")
        confirm_pass = st.text_input("Confirmar Contraseña", type="password", key="reg_confirm_pass")

        if st.button("Crear Empresa y Cuenta Maestro", use_container_width=True):
            # Validaciones de entrada previas
            if not (nombre_empresa and user_admin and pass_admin and nombre_admin):
                mostrar_notificacion("Registro Inválido", "Todos los campos son obligatorios.", es_error=True)
                return

            if pass_admin != confirm_pass:
                mostrar_notificacion("Registro Inválido", "Las contraseñas no coinciden.", es_error=True)
                return

            # --- BLOQUE DE OPERACIÓN ---
            try:
                # 1. Intentar insertar empresa
                query_d1("INSERT INTO empresas (nombre) VALUES (?)", [nombre_empresa])
                
                # 2. Obtener ID
                res_empresa = query_d1("SELECT id FROM empresas WHERE nombre = ?", [nombre_empresa])
                
                if res_empresa:
                    emp_id = res_empresa[0]['id']
                    # 3. Intentar insertar usuario
                    query_d1(
                        "INSERT INTO usuarios (username, password, empresa_id, rol, nombre_real) VALUES (?, ?, ?, ?, ?)",
                        [user_admin, pass_admin, emp_id, 'SuperAdmin', nombre_admin]
                    )
                    
                    # SI NO HAY EXCEPCIONES: Éxito (Verde)
                    mostrar_notificacion(
                        "Registro Exitoso", 
                        f"La empresa '{nombre_empresa}' ha sido creada correctamente.", 
                        es_error=False
                    )
                else:
                    mostrar_notificacion("Registro Inválido", "Error de comunicación con la base de datos.", es_error=True)

            except Exception as e:
                # CAPTURAMOS EL ERROR PARA QUE NO SALGA ABAJO
                error_raw = str(e)
                msg_final = "Error desconocido"
                
                if "UNIQUE constraint failed" in error_raw:
                    if "empresas.nombre" in error_raw:
                        msg_final = f"La empresa '{nombre_empresa}' ya existe."
                    elif "usuarios.username" in error_raw:
                        msg_final = f"El usuario '{user_admin}' ya está ocupado."
                else:
                    msg_final = f"Fallo técnico: {error_raw}"
                
                # Lanzamos el modal con Registro Inválido (Rojo)
                mostrar_notificacion("Registro Inválido", msg_final, es_error=True)