import streamlit as st
from modules import auth

def render_sidebar():
    """Sidebar principal de ORBERP con control de visibilidad y estilos."""
    
    # Estilos globales para limpieza de interfaz
    st.markdown("""
        <style>
            .stAppDeployButton {display:none;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header { background-color: rgba(0,0,0,0) !important; }
        </style>
    """, unsafe_allow_html=True)

    if 'tema_actual' not in st.session_state:
        st.session_state.tema_actual = "Claro"

    with st.sidebar:
        # Título actualizado a ORBERP
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
        opcion_tema = st.selectbox(
            "Seleccionar Modo", ["Claro", "Oscuro"],
            index=0 if st.session_state.tema_actual == "Oscuro" else 1,
            key="selector_tema_manual"
        )

        if opcion_tema != st.session_state.tema_actual:
            st.session_state.tema_actual = opcion_tema
            st.rerun()

        # Aplicación de Estilos Dinámicos
        if st.session_state.tema_actual == "Oscuro":
            aplicar_estilos_oscuros()
        else:
            aplicar_estilos_claros()

        st.divider()
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type="primary"):
            auth.logout()

        return seleccion

def aplicar_estilos_oscuros():
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: #FAFAFA; }
            [data-testid="stSidebar"] { background-color: #1A1C24; border-right: 1px solid #30363D; }
            .stTextInput>div>div>input { background-color: #0D1117 !important; color: white !important; }
            div[data-testid="stVerticalBlock"] > div[style*="border"] {
                background-color: #161B22 !important; border: 1px solid #30363D !important;
            }
        </style>
    """, unsafe_allow_html=True)

def aplicar_estilos_claros():
    """Modo Claro con visibilidad forzada"""
    st.markdown("""
        <style>
            .stApp { background-color: #F3F4F6 !important; color: #111827 !important; }
            h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText { color: #111827 !important; font-weight: 500 !important; }
            input, textarea, .stSelectbox, div[data-baseweb="select"] > div {
                background-color: #FFFFFF !important;
                color: #111827 !important;
                border: 1px solid #9CA3AF !important;
            }
            div[data-testid="stVerticalBlock"] > div[style*="border"] {
                background-color: #FFFFFF !important;
                border: 1px solid #D1D5DB !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
            }
            [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 2px solid #E5E7EB !important; }
            .stRadio label { color: #374151 !important; font-weight: 600 !important; }
        </style>
    """, unsafe_allow_html=True)