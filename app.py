import streamlit as st
from modules import auth, sidebar, inventario, administracion, compras, ventas, usuarios

# 1. Configuración de identidad del ERP
st.set_page_config(
    page_title="ORB ERP", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos globales para una interfaz limpia
st.markdown("""
    <style>
    .stAppDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header { background-color: rgba(0,0,0,0) !important; }
    
    /* Ajuste para que el contenido no pegue al techo */
    .block-container { padding-top: 1rem !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Gestión de Sesión (Estado Global)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. Lógica de acceso y enrutamiento
if not st.session_state.logged_in:
    # Pantalla de acceso a ALTO ERP
    auth.login_screen()
else:
    # Renderizamos el menú lateral (sidebar.py) que ya configuramos con temas
    opcion = sidebar.render_sidebar()

    # --- RUTEO DE MÓDULOS SEGMENTADOS ---
    
    if opcion == "📊 Dashboard":
        # Vista general de métricas
        administracion.render_dashboard()

    elif opcion == "📦 Inventario":
        # Gestión de productos y stock en la nube
        inventario.render_inventario()

    elif opcion == "🏢 Gestionar Departamentos":
        # Solo accesible por SuperAdmin (controlado en sidebar.py)
        administracion.render_gestion_departamentos()
        
    elif opcion == "👥 Gestionar Usuarios":
        usuarios.render_usuarios()

    elif opcion == "🛒 Ventas":
        ventas.render_ventas()

    elif opcion == "📥 Compras":
        compras.render_compras()