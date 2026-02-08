import streamlit as st
from modules import auth

def render_sidebar():
    """Sidebar principal de ORBERP con Modo Oscuro predeterminado."""
    
    # Estilos globales para limpieza de interfaz y forzado de fondo oscuro inicial
    st.markdown("""
        <style>
            .stAppDeployButton {display:none;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header { background-color: rgba(0,0,0,0) !important; }
            /* Evita el destello blanco al cargar */
            .stApp { background-color: #0E1117; }
        </style>
    """, unsafe_allow_html=True)

    # 1. ESTABLECER OSCURO POR DEFECTO
    if 'tema_actual' not in st.session_state:
        st.session_state.tema_actual = "Oscuro"

    with st.sidebar:
        nombre_empresa = st.session_state.get('empresa_nombre', 'ORBERP')
        st.markdown(f"### 🚀 {nombre_empresa}")
        
        with st.container(border=True):
            st.markdown(f"👤 **{st.session_state.get('nombre_real', 'Usuario')}**")
            st.caption(f"🔑 Rol: {st.session_state.get('rol', 'Acceso Base')}")
        
        st.divider()

        # --- NAVEGACIÓN ---
        menu_options = ["📊 Dashboard", "📦 Inventario"]
        
        if st.session_state.get('rol') == "SuperAdmin":
            menu_options.append("👥 Gestionar Usuarios")
        
        menu_options.extend(["🛒 Ventas", "📥 Compras"])
        
        seleccion = st.radio("Menú Principal", menu_options, key="nav_menu")

        st.divider()

        # --- APARIENCIA ---
        st.subheader("🎨 Apariencia")
        
        # Ajustamos el index para que por defecto marque "Oscuro"
        opcion_tema = st.selectbox(
            "Seleccionar Modo", 
            ["Claro", "Oscuro"],
            index=1, # 1 es "Oscuro"
            key="selector_tema_manual"
        )

        # Lógica de cambio de tema
        if opcion_tema != st.session_state.tema_actual:
            st.session_state.tema_actual = opcion_tema
            st.rerun()

        # Aplicación de Estilos
        if st.session_state.tema_actual == "Claro":
            aplicar_estilos_claros()
        else:
            aplicar_estilos_oscuros()

        st.divider()
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type="primary"):
            auth.logout()

        return seleccion

def aplicar_estilos_oscuros():
    """Modo Oscuro Premium para ORBERP"""
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
            [data-testid="stSidebar"] { 
                background-color: #1A1C24 !important; 
                border-right: 1px solid #30363D !important; 
            }
            /* Inputs y áreas de texto */
            .stTextInput>div>div>input, .stSelectbox>div>div { 
                background-color: #0D1117 !important; 
                color: white !important; 
                border: 1px solid #30363D !important;
            }
            /* Contenedores con borde */
            div[data-testid="stVerticalBlock"] > div[style*="border"] {
                background-color: #161B22 !important; 
                border: 1px solid #30363D !important;
            }
            /* Color de textos secundarios */
            .stMarkdown, p, label { color: #FAFAFA !important; }
        </style>
    """, unsafe_allow_html=True)

def aplicar_estilos_claros():
    """Modo Claro con visibilidad forzada"""
    st.markdown("""
        <style>
            .stApp { background-color: #F3F4F6 !important; color: #111827 !important; }
            h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText { color: #111827 !important; }
            [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 2px solid #E5E7EB !important; }
        </style>
    """, unsafe_allow_html=True)