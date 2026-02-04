import streamlit as st
import sqlite3
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sistema CVI - MultiEmpresa", layout="wide", page_icon="🏢")

# --- FUNCIONES DE BASE DE DATOS ---
def run_query(query, params=()):
    try:
        with sqlite3.connect('inventario.db') as conn:
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Error de lectura: {e}")
        return pd.DataFrame()

def execute_db(query, params=()):
    try:
        with sqlite3.connect('inventario.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        st.error(f"Error de escritura: {e}")
        return None

# --- LÓGICA DE SESIÓN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🛡️ Acceso al Sistema")
    tab_login, tab_reg = st.tabs(["🔐 Iniciar Sesión", "🚀 Registrar Mi Empresa"])

    with tab_login:
        with st.form("login_form"):
            # Ahora pedimos el nombre de la empresa para diferenciar usuarios repetidos
            form_empresa = st.text_input("Nombre de la Empresa")
            form_user = st.text_input("Usuario")
            form_pas = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Entrar al Panel"):
                # Buscamos al usuario que coincida con el nombre de usuario Y el nombre de su empresa
                query = """
                    SELECT u.*, e.nombre as empresa_nombre 
                    FROM usuarios u
                    JOIN empresas e ON u.empresa_id = e.id
                    WHERE e.nombre = ? AND u.username = ? AND u.password = ?
                """
                res = run_query(query, (form_empresa, form_user, form_pas))
                
                if not res.empty:
                    st.session_state.logged_in = True
                    st.session_state.user = form_user
                    st.session_state.empresa_id = int(res.iloc[0]['empresa_id'])
                    st.session_state.empresa_nombre = res.iloc[0]['empresa_nombre']
                    st.rerun()
                else:
                    st.error("Datos incorrectos. Verifica el nombre de la empresa y credenciales.")

    with tab_reg:
        with st.form("reg_form"):
            st.info("Crea un entorno único para tu negocio.")
            n_empresa = st.text_input("Nombre de la Empresa (Ej: Ferretería Central)")
            n_usuario = st.text_input("Usuario (Ej: admin)")
            n_pass = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Registrar Ahora"):
                if n_empresa and n_usuario and n_pass:
                    # 1. Validar que la empresa no exista
                    check_emp = run_query("SELECT id FROM empresas WHERE nombre = ?", (n_empresa,))
                    if check_emp.empty:
                        emp_id = execute_db("INSERT INTO empresas (nombre) VALUES (?)", (n_empresa,))
                        execute_db("INSERT INTO usuarios (username, password, empresa_id) VALUES (?, ?, ?)", 
                                   (n_usuario, n_pass, emp_id))
                        st.success(f"✅ ¡Listo! Usa '{n_empresa}' para loguearte.")
                    else:
                        st.error("Ese nombre de empresa ya está registrado.")
                else:
                    st.warning("Completa todos los campos.")

else:
    # --- PANEL DEL USUARIO ---
    st.sidebar.title(f"🏢 {st.session_state.empresa_nombre}")
    st.sidebar.write(f"👤 Usuario: **{st.session_state.user}**")
    
    opcion = st.sidebar.radio("Menú Principal", ["📦 Inventario", "🛒 Nueva Venta", "📥 Nueva Compra", "📈 Historial"])
    
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()

    # --- MÓDULOS ---
    if opcion == "📦 Inventario":
        st.header(f"📊 Panel de Control: {st.session_state.empresa_nombre}")
        
        # Consultas para métricas
        inv_df = run_query("SELECT nombre, stock, precio FROM productos WHERE empresa_id=?", 
                           (st.session_state.empresa_id,))
        
        if not inv_df.empty:
            # FILA DE MÉTRICAS
            col1, col2, col3 = st.columns(3)
            
            total_stock = inv_df['stock'].sum()
            valor_inventario = (inv_df['stock'] * inv_df['precio']).sum()
            productos_criticos = inv_df[inv_df['stock'] <= 5].shape[0]
            
            col1.metric("Unidades Totales", f"{total_stock:,}")
            col2.metric("Valor del Inventario", f"${valor_inventario:,.2f}")
            col3.metric("Productos en Crítico", f"{productos_criticos}", delta_color="inverse")

            # TABLA CON ALERTAS VISUALES
            st.subheader("Detalle de Existencias")
            
            # Aplicamos estilo: si el stock es < 5, resaltamos en rojo
            def color_stock(val):
                color = 'red' if val <= 5 else 'black'
                return f'color: {color}'

            st.dataframe(inv_df.style.applymap(color_stock, subset=['stock']), 
                         use_container_width=True, hide_index=True)
        else:
            st.info("El inventario está vacío. Comienza registrando una compra.")

    elif opcion == "🛒 Nueva Venta":
        st.header("Registrar Venta")
        prods = run_query("SELECT id, nombre, stock, precio FROM productos WHERE empresa_id=? AND stock > 0", 
                         (st.session_state.empresa_id,))
        
        if not prods.empty:
            with st.form("vta"):
                item = st.selectbox("Producto", prods['nombre'].tolist())
                cant = st.number_input("Cantidad", min_value=1, step=1)
                info = prods[prods['nombre'] == item].iloc[0]
                
                if st.form_submit_button("Confirmar Venta"):
                    if cant <= info['stock']:
                        execute_db("UPDATE productos SET stock = stock - ? WHERE id=?", (cant, info['id']))
                        execute_db("""INSERT INTO movimientos (producto_id, tipo, cantidad, precio_unitario, empresa_id) 
                                      VALUES (?, 'VENTA', ?, ?, ?)""", 
                                   (int(info['id']), cant, info['precio'], st.session_state.empresa_id))
                        st.success("Venta registrada.")
                        st.rerun()
                    else:
                        st.error("Stock insuficiente.")
        else:
            st.warning("Sin stock disponible.")

    elif opcion == "📥 Nueva Compra":
        st.header("Ingreso de Mercancía")
        with st.form("cmp"):
            nom = st.text_input("Producto")
            cant = st.number_input("Cantidad", min_value=1)
            pre = st.number_input("Costo Unitario", min_value=0.1)
            if st.form_submit_button("Guardar"):
                existente = run_query("SELECT id, stock FROM productos WHERE nombre=? AND empresa_id=?", 
                                     (nom, st.session_state.empresa_id))
                if not existente.empty:
                    p_id = int(existente.iloc[0]['id'])
                    execute_db("UPDATE productos SET stock=stock+?, precio=? WHERE id=?", (cant, pre, p_id))
                else:
                    p_id = execute_db("INSERT INTO productos (nombre, stock, precio, empresa_id) VALUES (?,?,?,?)", 
                                     (nom, cant, pre, st.session_state.empresa_id))
                
                execute_db("INSERT INTO movimientos (producto_id, tipo, cantidad, precio_unitario, empresa_id) VALUES (?, 'COMPRA', ?, ?, ?)",
                           (p_id, cant, pre, st.session_state.empresa_id))
                st.success("Inventario actualizado.")

    elif opcion == "📈 Historial":
        st.header("Reporte de Movimientos")
        query = """
            SELECT m.fecha, p.nombre, m.tipo, m.cantidad, m.precio_unitario, (m.cantidad * m.precio_unitario) as total
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            WHERE m.empresa_id = ?
            ORDER BY m.fecha DESC
        """
        st.dataframe(run_query(query, (st.session_state.empresa_id,)), use_container_width=True)