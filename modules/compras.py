import streamlit as st
from modules.database import query_d1

@st.dialog("Notificación de Sistema")
def mostrar_notificacion(titulo, detalle, es_error=False):
    if es_error:
        st.error(f"### ❌ Registro Inválido")
        st.markdown(f"**Detalle:** {detalle}")
        if st.button("Entendido", use_container_width=True, key="btn_comp_err"):
            st.rerun()
    else:
        st.success(f"### ✅ {titulo}")
        st.write(detalle)
        if st.button("Entendido", use_container_width=True, key="btn_comp_ok"):
            st.rerun()

@st.dialog("Detalle de la Compra")
def visor_detalle_compra(compra_id):
    """Muestra los productos específicos de la transacción."""
    sql = """
        SELECT p.nombre as 'Producto', d.cantidad as 'Cant.', d.precio_unitario as 'Precio U.',
               (d.cantidad * d.precio_unitario) as 'Subtotal'
        FROM detalle_compra d
        JOIN productos p ON d.producto_id = p.id
        WHERE d.compra_id = ?
    """
    detalles = query_d1(sql, [compra_id])
    if detalles:
        st.table(detalles)
        total = sum(item['Subtotal'] for item in detalles)
        st.markdown(f"#### **Total Pagado: ${total:,.2f}**")
    else:
        st.warning("No se encontraron detalles.")
    if st.button("Cerrar", use_container_width=True):
        st.rerun()

def render_compras():
    st.header("📥 Gestión de Compras - ORBERP")
    
    # --- FIX: Definición de variables de sesión ---
    empresa_id = st.session_state.get('empresa_id')
    usuario_id = st.session_state.get('user_id')

    # --- PARTE SUPERIOR: FORMULARIOS ---
    col_prov, col_comp = st.columns([1, 2])

    with col_prov:
        with st.expander("👤 Nuevo Proveedor", expanded=True):
            nom_prov = st.text_input("Nombre de Empresa", key="c_prov_nom")
            tel_prov = st.text_input("Teléfono", key="c_prov_tel")
            if st.button("💾 Guardar Proveedor", use_container_width=True):
                if nom_prov:
                    query_d1("INSERT INTO proveedores (nombre, telefono, empresa_id) VALUES (?, ?, ?)", 
                             [nom_prov, tel_prov, empresa_id])
                    mostrar_notificacion("Éxito", "Proveedor registrado.", es_error=False)
                else:
                    st.warning("Nombre obligatorio.")

    with col_comp:
        with st.expander("📝 Registrar Compra", expanded=True):
            provs = query_d1("SELECT id, nombre FROM proveedores WHERE empresa_id = ?", [empresa_id])
            prods = query_d1("SELECT id, nombre, precio_compra FROM productos WHERE empresa_id = ?", [empresa_id])
            
            dict_provs = {p['nombre']: p['id'] for p in provs} if provs else {}
            dict_prods = {p['nombre']: p['id'] for p in prods} if prods else {}
            
            c1, c2 = st.columns(2)
            prov_sel = c1.selectbox("Proveedor", options=list(dict_provs.keys()))
            prod_sel = c2.selectbox("Producto", options=list(dict_prods.keys()))
            cant = c1.number_input("Cantidad", min_value=1, step=1)
            precio = c2.number_input("Costo Unitario", min_value=0.0, format="%.2f")

            if st.button("🛒 Procesar Compra", use_container_width=True):
                if prov_sel and prod_sel:
                    try:
                        p_id = dict_prods[prod_sel]
                        pr_id = dict_provs[prov_sel]
                        total_compra = cant * precio
                        
                        # 1. Insertar encabezado y obtener ID (RETURNING id es para Cloudflare D1)
                        res = query_d1("INSERT INTO compras (proveedor_id, total, usuario_id, empresa_id) VALUES (?, ?, ?, ?) RETURNING id", 
                                       [pr_id, total_compra, usuario_id, empresa_id])
                        nueva_compra_id = res[0]['id']
                        
                        # 2. Insertar Detalle
                        query_d1("INSERT INTO detalle_compra (compra_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                                 [nueva_compra_id, p_id, cant, precio])
                        
                        # 3. Actualizar Inventario
                        query_d1("UPDATE productos SET stock = stock + ? WHERE id = ?", [cant, p_id])
                        
                        mostrar_notificacion("Compra Exitosa", f"Se registraron {cant} unidades.", es_error=False)
                    except Exception as e:
                        mostrar_notificacion("Error", str(e), es_error=True)

    st.divider()

    # --- PARTE INFERIOR: HISTORIAL ---
    st.subheader("📋 Historial de Compras")
    sql_h = """
        SELECT c.id, c.fecha as 'Fecha', p.nombre as 'Proveedor', c.total as 'Total'
        FROM compras c
        JOIN proveedores p ON c.proveedor_id = p.id
        WHERE c.empresa_id = ? ORDER BY c.fecha DESC
    """
    historial = query_d1(sql_h, [empresa_id])

    if historial:
        # Encabezados de tabla manual para permitir botones
        h_col1, h_col2, h_col3, h_col4 = st.columns([2, 3, 2, 1])
        h_col1.write("**Fecha**")
        h_col2.write("**Proveedor**")
        h_col3.write("**Monto ($)**")
        h_col4.write("**Ver**")

        for compra in historial:
            with st.container(border=False):
                r1, r2, r3, r4 = st.columns([2, 3, 2, 1])
                r1.write(compra['Fecha'])
                r2.write(compra['Proveedor'])
                r3.write(f"${compra['Total']:,.2f}")
                if r4.button("🔍", key=f"v_{compra['id']}"):
                    visor_detalle_compra(compra['id'])
    else:
        st.info("No hay registros de compras.")