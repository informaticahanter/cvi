import streamlit as st
from modules import auth, sidebar, inventario, administracion # Importamos el nuevo módulo

# 1. Configuración de página y ocultar menú de Streamlit
st.set_page_config(page_title="CVI System", layout="wide")

st.markdown("""
    <style>
    /* Ocultamos el botón de Deploy y el menú de Streamlit, pero NO el botón del sidebar */
    .stAppDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Mantenemos el header pero transparente para que la flecha del sidebar se vea */
    header {
        background-color: rgba(0,0,0,0) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Gestión de Sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. Lógica de acceso
if not st.session_state.logged_in:
    auth.login_screen()
else:
    # LLAMADA AL NUEVO DOCUMENTO DEL MENÚ (sidebar.py)
    opcion = sidebar.render_sidebar()

    # 4. Lógica de enrutamiento (Control de qué pantalla mostrar)
    if opcion == "📊 Dashboard":
        inventario.render_dashboard()
        
    elif opcion == "📦 Inventario":
        inventario.render_table()

    elif opcion == "🏢 Gestionar Departamentos":
        # Llamamos a la función del nuevo módulo administracion.py
        administracion.render_gestion_departamentos()
        
    elif opcion == "👥 Gestionar Usuarios":
        # Llamamos a la función de creación de usuarios por departamento
        administracion.render_gestion_usuarios()

    elif opcion == "🛒 Ventas":
        st.header("Módulo de Ventas")
        # ventas.render_form()

    elif opcion == "📥 Compras":
        st.header("Módulo de Compras")
        # compras.render_form()