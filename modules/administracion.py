import streamlit as st
from modules.database import query_d1
import pandas as pd

def render_dashboard():
    st.header("📊 Panel de Control - ORBERP")
    empresa_id = st.session_state.get('empresa_id')

    # 1. MÉTRICAS RÁPIDAS
    col1, col2, col3 = st.columns(3)
    
    total_ventas = query_d1("SELECT SUM(total) as total FROM ventas WHERE empresa_id = ?", [empresa_id])[0]['total'] or 0
    total_compras = query_d1("SELECT SUM(total) as total FROM compras WHERE empresa_id = ?", [empresa_id])[0]['total'] or 0
    prod_criticos = query_d1("SELECT COUNT(*) as cuenta FROM productos WHERE empresa_id = ? AND stock <= stock_minimo", [empresa_id])[0]['cuenta']

    col1.metric("Ingresos Totales", f"${total_ventas:,.2f}")
    col2.metric("Inversión en Compras", f"${total_compras:,.2f}")
    col3.metric("Alertas de Inventario", prod_criticos, delta_color="inverse")

    st.divider()

    # 2. ALERTAS Y GRÁFICOS
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("⚠️ Stock por Agotarse")
        stock_bajo = query_d1("SELECT nombre, stock, stock_minimo FROM productos WHERE empresa_id = ? AND stock <= stock_minimo LIMIT 5", [empresa_id])
        if stock_bajo:
            st.warning("Los siguientes productos requieren reposición inmediata:")
            st.table(stock_bajo)
        else:
            st.success("✅ Todo el inventario está en niveles óptimos.")

    with right_col:
        st.subheader("📈 Ventas Recientes")
        # Aquí simularíamos un gráfico con los datos de ventas
        ventas_data = query_d1("SELECT fecha, total FROM ventas WHERE empresa_id = ? ORDER BY fecha DESC LIMIT 10", [empresa_id])
        if ventas_data:
            df = pd.DataFrame(ventas_data)
            st.line_chart(df.set_index('fecha'))
        else:
            st.info("Aún no hay datos para graficar.")