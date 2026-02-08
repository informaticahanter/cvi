import streamlit as st
from modules import auth, sidebar, inventario, administracion, compras, ventas, usuarios, landing, registro_empresa

# 1. Configuración de identidad del ERP
st.set_page_config(
    page_title="ORBERP | Cloud Management", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos globales: Mantienen el diseño limpio y profesional
st.markdown("""
    <style>
    .stAppDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header { background-color: rgba(0,0,0,0) !important; }
    
    /* Eliminar el espacio superior excesivo en Streamlit */
    .block-container { padding-top: 1.5rem !important; }
    
    /* Estilo personalizado para los botones de retroceso */
    .stButton>button[kind="secondary"] {
        border-radius: 10px;
        color: #888;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Gestión de Sesión (Estado Global)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# IMPORTANTE: Aseguramos que 'vista_publica' exista siempre para el ruteo
if 'vista_publica' not in st.session_state:
    st.session_state.vista_publica = "landing"

# 3. Lógica de acceso y enrutamiento
if not st.session_state.logged_in:
    # --- ÁREA PÚBLICA: Landing, Login y Registro ---
    
    if st.session_state.vista_publica == "landing":
        landing.render_landing()
        
    elif st.session_state.vista_publica == "login":
        auth.login_screen()
        # Botón sutil para volver a la landing si el usuario se arrepiente
        st.write("") 
        if st.button("← Volver a la página principal", key="back_to_landing"):
            st.session_state.vista_publica = "landing"
            st.rerun()

    elif st.session_state.vista_publica == "registro_empresa":
        registro_empresa.render_registro()
        # Enlace rápido hacia el login desde el registro
        st.write("")
        if st.button("¿Ya tienes una empresa? Inicia sesión aquí", key="go_to_login"):
            st.session_state.vista_publica = "login"
            st.rerun()
else:
    # --- ÁREA PRIVADA: El ERP real después del acceso exitoso ---
    
    # Renderizamos el menú lateral y capturamos la opción elegida
    opcion = sidebar.render_sidebar()

    # Contenedor principal del Dashboard/Módulos
    with st.container():
        if opcion == "📊 Dashboard":
            administracion.render_dashboard()

        elif opcion == "📦 Inventario":
            inventario.render_inventario()

        elif opcion == "🏢 Gestionar Departamentos":
            administracion.render_gestion_departamentos()
            
        elif opcion == "👥 Gestionar Usuarios":
            usuarios.render_usuarios()

        elif opcion == "🛒 Ventas":
            ventas.render_ventas()

        elif opcion == "📥 Compras":
            compras.render_compras()
    
    # Botón de Cerrar Sesión (Ubicado en la parte inferior del Sidebar)
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
        # Limpiamos estados de sesión importantes al salir
        st.session_state.logged_in = False
        st.session_state.vista_publica = "landing"
        # Opcional: st.session_state.clear() si quieres borrar toda la RAM de la sesión
        st.rerun()