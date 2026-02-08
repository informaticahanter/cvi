import streamlit as st
from modules.database import query_d1

@st.dialog("Notificación de Sistema")
def mostrar_notificacion(titulo, detalle, es_error=False):
    if es_error:
        st.error(f"### ❌ Registro Inválido")
        st.markdown(f"**Detalle:** {detalle}")
        if st.button("Entendido", use_container_width=True, key="btn_inv_err"):
            st.rerun() 
    else:
        st.success(f"### ✅ {titulo}")
        st.write(detalle)
        if st.button("Entendido", use_container_width=True, key="btn_inv_ok"):
            st.rerun()

def render_inventario():
    st.header("📦 Gestión de Inventario - ORBERP")
    empresa_id = st.session_state.get('empresa_id')

    # --- PARTE SUPERIOR: FORMULARIOS ---
    col_form_prod, col_form_cat = st.columns([2, 1])

    with col_form_prod:
        with st.expander("➕ Agregar Nuevo Producto", expanded=True):
            res_cats = query_d1("SELECT id, nombre FROM categorias WHERE empresa_id = ?", [empresa_id])
            dict_cats = {c['nombre']: c['id'] for c in res_cats} if res_cats else {}
            
            with st.container():
                c1, c2 = st.columns(2)
                nombre = c1.text_input("Nombre", key="in_nom")
                sku = c2.text_input("SKU / Código", key="in_sku")
                
                cat_nom = c1.selectbox("Categoría", options=["Sin Categoría"] + list(dict_cats.keys()))
                stock = c2.number_input("Stock Inicial", min_value=0, step=1)
                
                p_compra = c1.number_input("Costo", min_value=0.0, format="%.2f")
                p_venta = c2.number_input("Venta", min_value=0.0, format="%.2f")
                
                s_minimo = st.number_input("Stock Mínimo", min_value=0, step=1)

                if st.button("💾 Guardar Producto", use_container_width=True):
                    if not (nombre and sku):
                        mostrar_notificacion("Campos Vacíos", "Nombre y SKU son obligatorios.", es_error=True)
                    else:
                        try:
                            cat_id = dict_cats.get(cat_nom)
                            sql = """INSERT INTO productos (nombre, sku, precio_compra, precio_venta, stock, stock_minimo, categoria_id, empresa_id) 
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                            query_d1(sql, [nombre, sku, p_compra, p_venta, stock, s_minimo, cat_id, empresa_id])
                            mostrar_notificacion("Éxito", "Producto registrado.", es_error=False)
                        except Exception as e:
                            mostrar_notificacion("Error", str(e), es_error=True)

    with col_form_cat:
        with st.expander("📁 Nueva Categoría", expanded=True):
            nueva_cat = st.text_input("Nombre de Categoría")
            if st.button("➕ Crear", use_container_width=True):
                if nueva_cat:
                    try:
                        query_d1("INSERT INTO categorias (nombre, empresa_id) VALUES (?, ?)", [nueva_cat, empresa_id])
                        mostrar_notificacion("Éxito", "Categoría creada.", es_error=False)
                    except Exception as e:
                        mostrar_notificacion("Error", str(e), es_error=True)
                else:
                    st.warning("Escribe un nombre")

    st.divider()

    # --- PARTE INFERIOR: TABLA DE STOCK ---
    st.subheader("📋 Lista de Stock Actual")
    
    # Nota: Si tu tabla SQL no tiene la columna 'sku', asegúrate de haber ejecutado el script SQL que te envié antes.
    sql_select = """
        SELECT p.sku as 'SKU', p.nombre as 'Producto', 
               COALESCE(c.nombre, 'Sin Categoría') as 'Categoría', 
               p.stock as 'Cantidad', p.precio_venta as 'Precio Venta'
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.empresa_id = ?
    """
    try:
        productos = query_d1(sql_select, [empresa_id])
        if productos:
            st.dataframe(productos, use_container_width=True, hide_index=True)
        else:
            st.info("No hay productos en el inventario.")
    except Exception as e:
        st.error(f"Error al cargar la lista: {str(e)}")