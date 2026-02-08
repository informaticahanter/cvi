import streamlit as st
from modules.database import query_d1

@st.dialog("Detalle de Venta")
def visor_detalle_venta(venta_id):
    sql = """
        SELECT p.nombre as 'Producto', d.cantidad as 'Cant.', d.precio_unitario as 'Precio U.', d.subtotal as 'Subtotal'
        FROM detalle_venta d
        JOIN productos p ON d.producto_id = p.id
        WHERE d.venta_id = ?
    """
    detalles = query_d1(sql, [venta_id])
    if detalles:
        st.table(detalles)
        total = sum(item['Subtotal'] for item in detalles)
        st.markdown(f"#### **Total Cobrado: ${total:,.2f}**")
    if st.button("Cerrar", use_container_width=True):
        st.rerun()

@st.dialog("Notificación ORBERP")
def mostrar_notificacion(titulo, detalle, es_error=False):
    if es_error:
        st.error(f"### ❌ Error")
        st.write(f"{detalle}")
    else:
        st.success(f"### ✅ {titulo}")
        st.write(detalle)
    if st.button("Entendido", use_container_width=True):
        st.rerun()

def render_ventas():
    st.header("🛒 Ventas y Clientes - ORBERP")
    empresa_id = st.session_state.get('empresa_id')
    usuario_id = st.session_state.get('user_id')

    # --- PARTE SUPERIOR: CLIENTES Y VENTA ---
    col_cli, col_ven = st.columns([1, 2])

    with col_cli:
        with st.expander("👤 Registro de Cliente", expanded=True):
            nom_cli = st.text_input("Nombre / Razón Social", key="v_cli_nom")
            id_cli = st.text_input("DNI / RUC", key="v_cli_id")
            if st.button("💾 Guardar Cliente", use_container_width=True):
                if nom_cli:
                    query_d1("INSERT INTO clientes (nombre, dni_ruc, empresa_id) VALUES (?, ?, ?)", 
                             [nom_cli, id_cli, empresa_id])
                    mostrar_notificacion("Éxito", "Cliente registrado.")
                else:
                    st.warning("El nombre es requerido.")

    with col_ven:
        with st.expander("📝 Nueva Venta", expanded=True):
            # Cargar Clientes y Productos
            clientes = query_d1("SELECT id, nombre FROM clientes WHERE empresa_id = ?", [empresa_id])
            prods = query_d1("SELECT id, nombre, precio_venta, stock FROM productos WHERE empresa_id = ? AND stock > 0", [empresa_id])
            
            dict_clis = {c['nombre']: c['id'] for c in clientes} if clientes else {"Venta Mostrador (General)": None}
            dict_prods = {f"{p['nombre']} (Stock: {p['stock']})": p for p in prods} if prods else {}

            c1, c2 = st.columns(2)
            cli_sel = c1.selectbox("Cliente", options=list(dict_clis.keys()))
            prod_sel_nom = c2.selectbox("Producto", options=list(dict_prods.keys()))
            
            if prod_sel_nom:
                p_data = dict_prods[prod_sel_nom]
                cant = c1.number_input("Cantidad", min_value=1, max_value=p_data['stock'], step=1)
                precio = c2.number_input("Precio", value=float(p_data['precio_venta']), format="%.2f")
                
                total_v = cant * precio
                st.subheader(f"Total: ${total_v:,.2f}")

                if st.button("🏁 Procesar Venta", use_container_width=True, type="primary"):
                    try:
                        c_id = dict_clis[cli_sel]
                        # 1. Encabezado de Venta (con cliente_id)
                        res = query_d1("INSERT INTO ventas (total, usuario_id, empresa_id, cliente_id) VALUES (?, ?, ?, ?) RETURNING id", 
                                       [total_v, usuario_id, empresa_id, c_id])
                        v_id = res[0]['id']

                        # 2. Detalle y Stock
                        query_d1("INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)",
                                 [v_id, p_data['id'], cant, precio, total_v])
                        query_d1("UPDATE productos SET stock = stock - ? WHERE id = ?", [cant, p_data['id']])
                        
                        mostrar_notificacion("Venta Realizada", f"Ticket #{v_id} para {cli_sel}")
                    except Exception as e:
                        mostrar_notificacion("Error", str(e), es_error=True)
            else:
                st.info("Sin stock disponible.")

    st.divider()

    # --- HISTORIAL DE VENTAS ---
    st.subheader("📋 Historial de Ventas")
    sql_h = """
        SELECT v.id, v.fecha as 'Fecha', IFNULL(c.nombre, 'Venta General') as 'Cliente', v.total as 'Total'
        FROM ventas v
        LEFT JOIN clientes c ON v.cliente_id = c.id
        WHERE v.empresa_id = ? ORDER BY v.fecha DESC
    """
    historial = query_d1(sql_h, [empresa_id])

    if historial:
        h_col1, h_col2, h_col3, h_col4 = st.columns([2, 3, 2, 1])
        h_col1.write("**Fecha**")
        h_col2.write("**Cliente**")
        h_col3.write("**Monto ($)**")
        h_col4.write("**Acción**")

        for v in historial:
            with st.container():
                r1, r2, r3, r4 = st.columns([2, 3, 2, 1])
                r1.write(v['Fecha'])
                r2.write(v['Cliente'])
                r3.write(f"${v['Total']:,.2f}")
                if r4.button("🔍", key=f"v_view_{v['id']}"):
                    visor_detalle_venta(v['id'])
    else:
        st.info("No hay ventas registradas.")