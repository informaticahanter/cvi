import streamlit as st

def render_landing():
    # CSS Avanzado y Premium para ORBERP
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
            
            /* Contenedor principal */
            .main { background-color: #050505; }
            
            /* Título Hero con Gradiente */
            .hero-title {
                font-size: clamp(2.5rem, 8vw, 4.5rem);
                font-weight: 800;
                background: linear-gradient(to right, #ffffff, #777777);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1.1;
                text-align: center;
                margin-bottom: 20px;
            }

            /* Grid de Funcionalidades */
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                padding: 40px 0;
            }

            /* Tarjetas con Efecto Glassmorphism */
            .card {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 35px;
                text-align: center;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }

            .card:hover {
                border-color: #ff4b4b;
                transform: translateY(-12px);
                background: rgba(255, 75, 75, 0.02);
                box-shadow: 0 15px 35px rgba(255, 75, 75, 0.1);
            }

            .card h3 { color: white; margin-bottom: 10px; font-size: 1.5rem; }
            .card p { color: #888; line-height: 1.6; }

            /* Ajuste de Botones Streamlit */
            div.stButton > button {
                border-radius: 12px !important;
                font-weight: 600 !important;
                transition: 0.3s !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- NAVBAR ---
    nav_col1, nav_col2, nav_col3 = st.columns([3, 1, 1])
    
    with nav_col1:
        st.markdown("<h2 style='margin:0; color:white;'>🚀 <b>ORBERP</b></h2>", unsafe_allow_html=True)
    
    with nav_col2:
        # Redirige a la pantalla de login en app.py
        if st.button("Ingresar", key="nav_login_main", use_container_width=True):
            st.session_state.vista_publica = "login"
            st.rerun()
        
    with nav_col3:
        # Redirige a la pantalla de registro en app.py
        if st.button("Registrar", type="primary", key="nav_reg_main", use_container_width=True):
            st.session_state.vista_publica = "registro_empresa"
            st.rerun()

    # --- HERO SECTION ---
    st.write("#")
    st.markdown('<h1 class="hero-title">Gestión Inteligente.<br>Escalabilidad Real.</h1>', unsafe_allow_html=True)
    st.markdown("""
        <p style="color: #aaa; text-align: center; font-size: 1.2rem; max-width: 750px; margin: 0 auto;">
            La plataforma integral para el control de inventarios, ventas y departamentos. 
            Diseñada para empresas que no se detienen.
        </p>
    """, unsafe_allow_html=True)

    st.write("#")
    
    # Botón Call to Action Central
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("🔥 Empieza tu Transformación", use_container_width=True, key="hero_cta_btn"):
            st.session_state.vista_publica = "registro_empresa"
            st.rerun()

    st.write("#")
    st.divider()

    # --- FEATURES SECTION ---
    st.markdown("""
        <div class="features-grid">
            <div class="card">
                <div style="font-size: 40px; margin-bottom: 15px;">📦</div>
                <h3>Stock Pro</h3>
                <p>Control de existencias en tiempo real con alertas automáticas de stock bajo.</p>
            </div>
            <div class="card">
                <div style="font-size: 40px; margin-bottom: 15px;">⚡</div>
                <h3>Venta Express</h3>
                <p>Punto de venta optimizado para máxima velocidad en cada transacción.</p>
            </div>
            <div class="card">
                <div style="font-size: 40px; margin-bottom: 15px;">📊</div>
                <h3>Analítica</h3>
                <p>Toma decisiones basadas en datos con nuestros tableros de rendimiento.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer Sutil
    st.write("---")
    st.markdown("<p style='text-align:center; color:#555; padding-bottom: 20px;'>© 2026 ORBERP Business Cloud. Todos los derechos reservados.</p>", unsafe_allow_html=True)