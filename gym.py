import tkinter as tk
from tkinter import ttk 
import sqlite3
from tkinter import messagebox

# ==================================================================
# CONEXIÓN A LA BASE DE DATOS ÚNICA
# ==================================================================
conect = sqlite3.connect("mariagym.db") 
cursor = conect.cursor()

# Tabla de Usuarios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL
    )
""")

# Tabla de Productos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        precio REAL NOT NULL
    )
""")

# Tabla de ventas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        precio REAL NOT NULL
    )
""")
conect.commit()

# Variables globales para rastrear las ediciones independientes
usuario_id_actualizar = None
producto_id_actualizar = None
venta_id_actualizar = None 
inventario_id_actualizar = None

# ==================================================================
# VENTANAS DE LA INTERFAZ
# ==================================================================
ventanai = tk.Tk()
ventanai.title("mariagym")
ventanai.geometry("500x400")

# --- SUBVENTANAS DE PRODUCTOS ---
ventanap = tk.Toplevel(ventanai)
ventanap.title("Productos - Menú")
ventanap.geometry("400x350")
ventanap.withdraw() 

ventanaC_prod = tk.Toplevel(ventanap)
ventanaC_prod.title("Agregar Producto")
ventanaC_prod.geometry("400x350")
ventanaC_prod.withdraw()

ventanar_prod = tk.Toplevel(ventanap)
ventanar_prod.title("Buscar Producto")
ventanar_prod.geometry("400x350")
ventanar_prod.withdraw()

ventanau_prod = tk.Toplevel(ventanap)
ventanau_prod.title("Actualizar Producto")
ventanau_prod.geometry("400x450")
ventanau_prod.withdraw()

ventanae_prod = tk.Toplevel(ventanap)
ventanae_prod.title("Eliminar Producto")
ventanae_prod.geometry("400x350")
ventanae_prod.withdraw()

# --- SUBVENTANAS DE USUARIOS ---
ventanam = tk.Toplevel(ventanai)
ventanam.title("CRUD Usuarios")
ventanam.geometry("300x250")
ventanam.withdraw() 

ventanaC = tk.Toplevel(ventanam)
ventanaC.title("Almacen")
ventanaC.geometry("400x350")
ventanaC.withdraw()

ventanar = tk.Toplevel(ventanam)
ventanar.title("Mostrar Usuarios")
ventanar.geometry("400x350")
ventanar.withdraw()

ventanau = tk.Toplevel(ventanam)
ventanau.title("Actualizar Usuarios")
ventanau.geometry("400x420")
ventanau.withdraw()

ventanae = tk.Toplevel(ventanam)
ventanae.title("Eliminar Usuarios")
ventanae.geometry("400x350")
ventanae.withdraw()

# --- SUBVENTANAS DE VENTAS ---
ventanav = tk.Toplevel(ventanai)
ventanav.title("Ventas - Menú")
ventanav.geometry("400x350")
ventanav.withdraw() 

ventanaC_ven = tk.Toplevel(ventanav)
ventanaC_ven.title("Agregar Venta")
ventanaC_ven.geometry("400x350")
ventanaC_ven.withdraw()

ventanar_ven = tk.Toplevel(ventanav)
ventanar_ven.title("Buscar Venta")
ventanar_ven.geometry("400x350")
ventanar_ven.withdraw()

ventanau_ven = tk.Toplevel(ventanav)
ventanau_ven.title("Actualizar Venta")
ventanau_ven.geometry("400x450")
ventanau_ven.withdraw()

ventanae_ven = tk.Toplevel(ventanav)
ventanae_ven.title("Eliminar Venta")
ventanae_ven.geometry("400x350")
ventanae_ven.withdraw()

ventanainv = tk.Toplevel(ventanai)
ventanainv.title("Inventario - Historial de Ventas")
ventanainv.geometry("400x350")
ventanainv.withdraw()

ventanainv_table = tk.Toplevel(ventanai)
ventanainv_table.title("Inventario - Tabla de Ventas")
ventanainv_table.geometry("550x450")
ventanainv_table.withdraw()

# ==================================================================
# FUNCIONES: MÓDULO USUARIOS
# ==================================================================
def crear_usuario():
    nombre = entry_nombre.get().strip()
    edad_texto = entry_edad.get().strip()
    
    if not nombre or not edad_texto:
        messagebox.showwarning("advertencia", "Por favor llena todos los campos.")
        return
    try:
        edad = int(edad_texto) 
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número entero.")
        return

    if edad < 14:
        messagebox.showwarning("advertencia", "No puedes ingresar al almacen, eres menor.")
        return
    
    cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", (nombre, edad))
    conect.commit()    
    
    id_generado = cursor.lastrowid
    messagebox.showinfo("Éxito", f"Usuario creado: {nombre}, Edad: {edad} | ID: {id_generado}")
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)

def buscar_usuario():
    id_busqueda = entry_id.get().strip()
    if not id_busqueda:
        messagebox.showwarning("advertencia", "ingresa un ID para buscar.")
        return

    cursor_busqueda = conect.cursor()
    cursor_busqueda.execute("SELECT * FROM usuarios WHERE id = ?", (id_busqueda,))
    datos = cursor_busqueda.fetchone() 
    cursor_busqueda.close()

    if datos:
        lbl_info_busqueda.config(text=f"ID: {datos[0]}\nNombre: {datos[1]}\nEdad: {datos[2]} años", fg="black")
    else:
        lbl_info_busqueda.config(text="Usuario no encontrado.", fg="red")

def editar_usuario():
    global usuario_id_actualizar
    id_busqueda = entry_mod_id.get().strip()

    if not id_busqueda:
        messagebox.showwarning("advertencia", "ingresa el ID del usuario que deseas editar")
        return

    cursor_busqueda = conect.cursor()
    cursor_busqueda.execute("SELECT * FROM usuarios WHERE id = ?", (id_busqueda,))
    datos = cursor_busqueda.fetchone()
    cursor_busqueda.close()

    if datos:
        usuario_id_actualizar = datos[0]
        lbl_status_edicion.config(text=f"Editando ID: {datos[0]}", fg="green")
        entry_mod_nombre.delete(0, tk.END)
        entry_mod_nombre.insert(0, datos[1])
        entry_mod_edad.delete(0, tk.END)
        entry_mod_edad.insert(0, str(datos[2]))
    else:
        usuario_id_actualizar = None
        lbl_status_edicion.config(text="Usuario no encontrado para editar.", fg="red")
        entry_mod_nombre.delete(0, tk.END)
        entry_mod_edad.delete(0, tk.END)

def actualizar_usuario():
    global usuario_id_actualizar
    if usuario_id_actualizar is None:
        messagebox.showwarning("advertencia", "Primero carga un usuario para editar.")
        return

    nuevo_nombre = entry_mod_nombre.get().strip()
    nuevo_edad_texto = entry_mod_edad.get().strip()

    if not nuevo_nombre or not nuevo_edad_texto:
        messagebox.showwarning("advertencia", "Por favor llena todos los campos.")
        return
    try:
        nueva_edad = int(nuevo_edad_texto)
    except ValueError:
        messagebox.showwarning("advertencia", "Por favor ingresa una edad válida.")
        return

    if nueva_edad < 14:
        messagebox.showwarning("restriccion", "la edad debe ser mayor a 14 años.")
        return

    cursor.execute("UPDATE usuarios SET nombre = ?, edad= ? WHERE id = ?", (nuevo_nombre, nueva_edad, usuario_id_actualizar))
    conect.commit()

    messagebox.showinfo("Exito","Usuario actualizado correctamente")
    limpiar_ventana_editar_usuario()
    volver_al_menu(ventanau, ventanam)

def eliminar_usuario():
    id_eliminar = entry_del_id.get().strip()
    if not id_eliminar:
        messagebox.showwarning("advertencia", "ingresa el ID del usuario que deseas eliminar")
        return

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_eliminar,))
    conect.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Exito", f"Usuario con ID {id_eliminar} eliminado.")
    else:
        messagebox.showwarning("No encontrado", f"No se encontró un usuario con ID {id_eliminar}.")
    entry_del_id.delete(0, tk.END)

def limpiar_ventana_editar_usuario():
    global usuario_id_actualizar
    usuario_id_actualizar = None
    entry_mod_id.delete(0, tk.END)
    entry_mod_nombre.delete(0, tk.END)
    entry_mod_edad.delete(0, tk.END)
    lbl_status_edicion.config(text="Introduce un ID y presiona 'Cargar Datos'", fg="gray")


# ==================================================================
# FUNCIONES: MÓDULO PRODUCTOS
# ==================================================================
def crear_producto():
    nombre = entry_p_nombre.get().strip()
    desc = entry_p_desc.get().strip()
    precio_txt = entry_p_precio.get().strip()
    
    if not nombre or not desc or not precio_txt:
        messagebox.showwarning("Advertencia", "Por favor llena todos los campos.")
        return
    try:
        precio = float(precio_txt)
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número decimal.")
        return

    cursor.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)", (nombre, desc, precio))
    conect.commit()
    
    messagebox.showinfo("Éxito", f"Producto agregado: {nombre} | ID: {cursor.lastrowid}")
    entry_p_nombre.delete(0, tk.END)
    entry_p_desc.delete(0, tk.END)
    entry_p_precio.delete(0, tk.END)

def buscar_producto():
    id_b = entry_p_id.get().strip()
    if not id_b:
        messagebox.showwarning("Advertencia", "Ingresa un ID de producto.")
        return

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_b,))
    datos = cursor.fetchone()
    if datos:
        lbl_res_prod.config(text=f"ID: {datos[0]}\nNombre: {datos[1]}\nDesc: {datos[2]}\nPrecio: ${datos[3]:.2f}", fg="black")
    else:
        lbl_res_prod.config(text="Producto no encontrado.", fg="red")

def cargar_producto():
    global producto_id_actualizar
    id_b = entry_mod_pid.get().strip()
    if not id_b:
        messagebox.showwarning("Advertencia", "Ingresa el ID del producto.")
        return

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_b,))
    datos = cursor.fetchone()
    if datos:
        producto_id_actualizar = datos[0]
        lbl_status_p.config(text=f"Editando Producto ID: {datos[0]}", fg="green")
        entry_mod_pnombre.delete(0, tk.END)
        entry_mod_pnombre.insert(0, datos[1])
        entry_mod_pdesc.delete(0, tk.END)
        entry_mod_pdesc.insert(0, datos[2])
        entry_mod_pprecio.delete(0, tk.END)
        entry_mod_pprecio.insert(0, str(datos[3]))
    else:
        producto_id_actualizar = None
        lbl_status_p.config(text="Producto no encontrado.", fg="red")

def actualizar_producto():
    global producto_id_actualizar
    if producto_id_actualizar is None:
        messagebox.showwarning("Advertencia", "Primero carga un producto.")
        return

    n_nombre = entry_mod_pnombre.get().strip()
    n_desc = entry_mod_pdesc.get().strip()
    n_precio_txt = entry_mod_pprecio.get().strip()

    if not n_nombre or not n_desc or not n_precio_txt:
        messagebox.showwarning("Advertencia", "Llena todos los campos.")
        return
    try:
        n_precio = float(n_precio_txt)
    except ValueError:
        messagebox.showerror("Error", "Precio inválido.")
        return

    cursor.execute("UPDATE productos SET nombre=?, descripcion=?, precio=? WHERE id=?", (n_nombre, n_desc, n_precio, producto_id_actualizar))
    conect.commit()
    
    messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
    limpiar_ventana_editar_producto()
    volver_al_menu(ventanau_prod, ventanap)

def eliminar_producto():
    id_del = entry_del_pid.get().strip()
    if not id_del:
        messagebox.showwarning("Advertencia", "Ingresa el ID a eliminar.")
        return
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_del,))
    conect.commit()
    if cursor.rowcount > 0:
        messagebox.showinfo("Éxito", f"Producto ID {id_del} eliminado.")
    else:
        messagebox.showwarning("Error", "ID no encontrado.")
    entry_del_pid.delete(0, tk.END)

def limpiar_ventana_editar_producto():
    global producto_id_actualizar
    producto_id_actualizar = None
    entry_mod_pid.delete(0, tk.END)
    entry_mod_pnombre.delete(0, tk.END)
    entry_mod_pdesc.delete(0, tk.END)
    entry_mod_pprecio.delete(0, tk.END)
    lbl_status_p.config(text="Introduce un ID y presiona 'Cargar Datos'", fg="gray")


# ==================================================================
# FUNCIONES: MÓDULO VENTAS
# ==================================================================
def crear_venta():
    nombrev = entry_usuario.get().strip()
    descv = entry_v_desc.get().strip()
    preciov_txt = entry_v_precio.get().strip()
    
    if not nombrev or not descv or not preciov_txt:
        messagebox.showwarning("Advertencia", "Por favor llena todos los campos.")
        return
    try:
        preciov = float(preciov_txt)
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número decimal.")
        return

    cursor.execute("INSERT INTO ventas (usuario, descripcion, precio) VALUES (?, ?, ?)", (nombrev, descv, preciov))
    conect.commit()
    
    messagebox.showinfo("Éxito", f"Venta agregada para: {nombrev} | ID: {cursor.lastrowid}")
    entry_usuario.delete(0, tk.END)
    entry_v_desc.delete(0, tk.END)
    entry_v_precio.delete(0, tk.END)

def buscar_venta():
    id_b = entry_v_id.get().strip()
    if not id_b:
        messagebox.showwarning("Advertencia", "Ingresa un ID de venta.")
        return

    cursor.execute("SELECT * FROM ventas WHERE id = ?", (id_b,))
    datos = cursor.fetchone()
    if datos:
        lbl_res_vent.config(text=f"ID: {datos[0]}\nUsuario: {datos[1]}\nDesc: {datos[2]}\nPrecio: ${datos[3]:.2f}", fg="black")
    else:
        lbl_res_vent.config(text="Venta no encontrada.", fg="red")

def cargar_venta():
    global venta_id_actualizar
    id_v = entry_mod_vid.get().strip()
    if not id_v:
        messagebox.showwarning("Advertencia", "Ingresa el ID de la venta.")
        return

    cursor.execute("SELECT * FROM ventas WHERE id = ?", (id_v,))
    datos = cursor.fetchone()
    if datos:
        venta_id_actualizar = datos[0]
        lbl_status_v.config(text=f"Editando Venta ID: {datos[0]}", fg="green")
        entry_mod_vnombre.delete(0, tk.END)
        entry_mod_vnombre.insert(0, datos[1])
        entry_mod_vdesc.delete(0, tk.END)
        entry_mod_vdesc.insert(0, datos[2])
        entry_mod_vprecio.delete(0, tk.END)
        entry_mod_vprecio.insert(0, str(datos[3]))
    else:
        venta_id_actualizar = None
        lbl_status_v.config(text="Venta no encontrada.", fg="red")

def actualizar_venta():
    global venta_id_actualizar
    if venta_id_actualizar is None:
        messagebox.showwarning("Advertencia", "Primero carga una venta.")
        return

    v_nombre = entry_mod_vnombre.get().strip()
    v_desc = entry_mod_vdesc.get().strip()
    v_precio_txt = entry_mod_vprecio.get().strip()

    if not v_nombre or not v_desc or not v_precio_txt:
        messagebox.showwarning("Advertencia", "Llena todos los campos.")
        return
    try:
        v_precio = float(v_precio_txt)
    except ValueError:
        messagebox.showerror("Error", "Precio inválido.")
        return

    cursor.execute("UPDATE ventas SET usuario=?, descripcion=?, precio=? WHERE id=?", (v_nombre, v_desc, v_precio, venta_id_actualizar))
    conect.commit()
    
    messagebox.showinfo("Éxito", "Venta actualizada correctamente.")
    limpiar_ventana_editar_venta()
    volver_al_menu(ventanau_ven, ventanav) 

def eliminar_venta():
    id_del = entry_del_vid.get().strip()
    if not id_del:
        messagebox.showwarning("Advertencia", "Ingresa el ID a eliminar.")
        return
    cursor.execute("DELETE FROM ventas WHERE id = ?", (id_del,))
    conect.commit()
    if cursor.rowcount > 0:
        messagebox.showinfo("Éxito", f"Venta ID {id_del} eliminada.")
    else:
        messagebox.showwarning("Error", "ID no encontrado.")
    entry_del_vid.delete(0, tk.END)

def limpiar_ventana_editar_venta():
    global venta_id_actualizar
    venta_id_actualizar = None
    entry_mod_vid.delete(0, tk.END)
    entry_mod_vnombre.delete(0, tk.END)
    entry_mod_vdesc.delete(0, tk.END)
    entry_mod_vprecio.delete(0, tk.END)
    lbl_status_v.config(text="Introduce un ID y presiona 'Cargar Datos'", fg="gray")


# ==================================================================
# MÓDULO NUEVO: FUNCIÓN PARA LLENAR LA TABLA DE INVENTARIO
# ==================================================================
def mostrar_ventas_inventario():
    """Consulta los datos de la tabla 'ventas' y actualiza el Frame visual"""
    for fila in tabla_ventas.get_children():
        tabla_ventas.delete(fila)
        
    cursor_inv = conect.cursor()
    cursor_inv.execute("SELECT * FROM ventas")
    registros = cursor_inv.fetchall()
    cursor_inv.close()
    
    for r in registros:
    
        tabla_ventas.insert("", tk.END, values=(r[0], r[1], r[2], f"${r[3]:.2f}"))


# ==================================================================
# 6. NAVEGACIÓN DE VENTANAS
# ==================================================================
def abrir_seccion(ventana_abrir, ventana_cerrar):
    ventana_abrir.deiconify()
    ventana_cerrar.withdraw()

def volver_al_menu(ventana_actual, menu_anterior):
    ventana_actual.withdraw()
    menu_anterior.deiconify()


# ==================================================================
# COMPONENTES GRÁFICOS (WIDGETS)
# ==================================================================

# --- VENTANA DE INICIO ---
tk.Label(ventanai, text="Bienvenid@ a Gymforce", font=("Arial", 14, "bold")).pack(pady=20)
tk.Button(ventanai, text="Usuarios", command=lambda: abrir_seccion(ventanam, ventanai), bg="lightblue", width=15).pack(pady=10)
tk.Button(ventanai, text="Productos", command=lambda: abrir_seccion(ventanap, ventanai), bg="lightgreen", width=15).pack(pady=10)
tk.Button(ventanai, text="Ventas", command=lambda: abrir_seccion(ventanav, ventanai), bg="lightcoral", width=15).pack(pady=10)
tk.Button(ventanai, text="Inventario", command=lambda: [abrir_seccion(ventanainv, ventanai), mostrar_ventas_inventario()], bg="khaki", width=15).pack(pady=10)
tk.Button(ventanai, text="Salir", command=ventanai.destroy, bg="salmon", width=15).pack(pady=20)

# --- MENÚ USUARIOS ---
tk.Button(ventanam, text="Crear Usuario", command=lambda: abrir_seccion(ventanaC, ventanam)).pack(pady=5)
tk.Button(ventanam, text="Buscar Usuarios", command=lambda: abrir_seccion(ventanar, ventanam)).pack(pady=5)
tk.Button(ventanam, text="Editar Usuarios", command=lambda: abrir_seccion(ventanau, ventanam)).pack(pady=5) 
tk.Button(ventanam, text="Eliminar Usuarios", command=lambda: abrir_seccion(ventanae, ventanam)).pack(pady=5)
tk.Button(ventanam, text="Volver al Inicio", command=lambda: volver_al_menu(ventanam, ventanai)).pack(pady=10)

# --- MENÚ PRODUCTOS ---
tk.Button(ventanap, text="Agregar Producto", command=lambda: abrir_seccion(ventanaC_prod, ventanap), bg="lightyellow").pack(pady=5)
tk.Button(ventanap, text="Buscar Producto", command=lambda: abrir_seccion(ventanar_prod, ventanap), bg="lightyellow").pack(pady=5)
tk.Button(ventanap, text="Editar Producto", command=lambda: abrir_seccion(ventanau_prod, ventanap), bg="lightyellow").pack(pady=5)
tk.Button(ventanap, text="Eliminar Producto", command=lambda: abrir_seccion(ventanae_prod, ventanap), bg="lightyellow").pack(pady=5)
tk.Button(ventanap, text="Volver al Inicio", command=lambda: volver_al_menu(ventanap, ventanai)).pack(pady=10)

# --- MENÚ VENTAS ---
tk.Button(ventanav, text="Agregar Venta", command=lambda: abrir_seccion(ventanaC_ven, ventanav), bg="lightyellow").pack(pady=5)
tk.Button(ventanav, text="Buscar Venta", command=lambda: abrir_seccion(ventanar_ven, ventanav), bg="lightyellow").pack(pady=5)
tk.Button(ventanav, text="Actualizar Venta", command=lambda: abrir_seccion(ventanau_ven, ventanav), bg="lightyellow").pack(pady=5)
tk.Button(ventanav, text="Eliminar Venta", command=lambda: abrir_seccion(ventanae_ven, ventanav), bg="lightyellow").pack(pady=5)
tk.Button(ventanav, text="Volver al Inicio", command=lambda: volver_al_menu(ventanav, ventanai)).pack(pady=10)


# --- SUBVENTANAS USUARIOS ---
# Crear Usuario
tk.Label(ventanaC, text="Crear un nuevo usuario", font=("Arial", 11, "bold")).pack(pady=5)
entry_nombre = tk.Entry(ventanaC, width=30); entry_nombre.pack(pady=2)
entry_edad = tk.Entry(ventanaC, width=10); entry_edad.pack(pady=2)
tk.Button(ventanaC, text="Guardar Usuario", command=crear_usuario, bg="lightgreen").pack(pady=5)
tk.Button(ventanaC, text="Volver al Menú", command=lambda: volver_al_menu(ventanaC, ventanam)).pack()

# Buscar Usuario
tk.Label(ventanar, text="Buscar datos", font=("Arial", 11, "bold")).pack(pady=5)
entry_id = tk.Entry(ventanar, width=15); entry_id.pack(pady=5)
tk.Button(ventanar, text="Buscar ID", command=buscar_usuario, bg="lightblue").pack(pady=5)
lbl_info_busqueda = tk.Label(ventanar, text="Los resultados aparecerán aquí", fg="gray"); lbl_info_busqueda.pack(pady=5)
tk.Button(ventanar, text="Volver al Menú", command=lambda: volver_al_menu(ventanar, ventanam)).pack()

# Actualizar Usuario
tk.Label(ventanau, text="Actualizar usuario", font=("Arial", 11, "bold")).pack(pady=5)
entry_mod_id = tk.Entry(ventanau, width=15); entry_mod_id.pack(pady=5)
tk.Button(ventanau, text="Cargar Datos", command=editar_usuario, bg="lightblue").pack(pady=5)
lbl_status_edicion = tk.Label(ventanau, text="Introduce un ID y presiona 'Cargar Datos'", fg="gray"); lbl_status_edicion.pack(pady=5)
tk.Frame(ventanau, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)
entry_mod_nombre = tk.Entry(ventanau, width=30); entry_mod_nombre.pack(pady=2)
entry_mod_edad = tk.Entry(ventanau, width=10); entry_mod_edad.pack(pady=2)
tk.Button(ventanau, text="Actualizar Usuario", command=actualizar_usuario, bg="lightgreen").pack(pady=5)
tk.Button(ventanau, text="Cancelar", command=lambda: [limpiar_ventana_editar_usuario(), volver_al_menu(ventanau, ventanam)]).pack()

# Eliminar Usuario
tk.Label(ventanae, text="Eliminar usuario por ID", font=("Arial", 11, "bold")).pack(pady=5)
entry_del_id = tk.Entry(ventanae, width=15); entry_del_id.pack(pady=5)
tk.Button(ventanae, text="Eliminar Usuario", command=eliminar_usuario, bg="salmon").pack(pady=5)
tk.Button(ventanae, text="Volver al Menú", command=lambda: volver_al_menu(ventanae, ventanam)).pack()


# --- SUBVENTANAS PRODUCTOS ---
# Agregar Producto
tk.Label(ventanaC_prod, text="Agregar Nuevo Producto", font=("Arial", 11, "bold")).pack(pady=5)
tk.Label(ventanaC_prod, text="Nombre del Producto:").pack()
entry_p_nombre = tk.Entry(ventanaC_prod, width=30); entry_p_nombre.pack(pady=2)
tk.Label(ventanaC_prod, text="Descripción:").pack()
entry_p_desc = tk.Entry(ventanaC_prod, width=30); entry_p_desc.pack(pady=2)
tk.Label(ventanaC_prod, text="Precio:").pack()
entry_p_precio = tk.Entry(ventanaC_prod, width=10); entry_p_precio.pack(pady=2)
tk.Button(ventanaC_prod, text="Guardar Producto", command=crear_producto, bg="lightgreen").pack(pady=5)
tk.Button(ventanaC_prod, text="Volver", command=lambda: volver_al_menu(ventanaC_prod, ventanap)).pack()

# Buscar Producto
tk.Label(ventanar_prod, text="Buscar Producto por ID", font=("Arial", 11, "bold")).pack(pady=5)
entry_p_id = tk.Entry(ventanar_prod, width=15); entry_p_id.pack(pady=5)
tk.Button(ventanar_prod, text="Buscar Producto", command=buscar_producto, bg="lightblue").pack(pady=5)
lbl_res_prod = tk.Label(ventanar_prod, text="Los resultados aparecerán aquí", fg="gray"); lbl_res_prod.pack(pady=5)
tk.Button(ventanar_prod, text="Volver", command=lambda: volver_al_menu(ventanar_prod, ventanap)).pack()

# Actualizar Producto
tk.Label(ventanau_prod, text="Modificar Datos de Producto", font=("Arial", 11, "bold")).pack(pady=5)
entry_mod_pid = tk.Entry(ventanau_prod, width=15); entry_mod_pid.pack(pady=5)
tk.Button(ventanau_prod, text="Cargar Datos", command=cargar_producto, bg="lightblue").pack(pady=5)
lbl_status_p = tk.Label(ventanau_prod, text="Introduce un ID y presiona 'Cargar Datos'", fg="gray"); lbl_status_p.pack(pady=5)
tk.Frame(ventanau_prod, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)
tk.Label(ventanau_prod, text="Nuevo Nombre:").pack()
entry_mod_pnombre = tk.Entry(ventanau_prod, width=30); entry_mod_pnombre.pack(pady=2)
tk.Label(ventanau_prod, text="Nueva Descripción:").pack()
entry_mod_pdesc = tk.Entry(ventanau_prod, width=30); entry_mod_pdesc.pack(pady=2)
tk.Label(ventanau_prod, text="Nuevo Precio:").pack()
entry_mod_pprecio = tk.Entry(ventanau_prod, width=10); entry_mod_pprecio.pack(pady=2)
tk.Button(ventanau_prod, text="Actualizar Producto", command=actualizar_producto, bg="lightgreen").pack(pady=5)
tk.Button(ventanau_prod, text="Cancelar", command=lambda: [limpiar_ventana_editar_producto(), volver_al_menu(ventanau_prod, ventanap)]).pack()

# Eliminar Producto
tk.Label(ventanae_prod, text="Eliminar Producto por ID", font=("Arial", 11, "bold")).pack(pady=5)
entry_del_pid = tk.Entry(ventanae_prod, width=15); entry_del_pid.pack(pady=5)
tk.Button(ventanae_prod, text="Eliminar Producto", command=eliminar_producto, bg="salmon").pack(pady=5)
tk.Button(ventanae_prod, text="Volver", command=lambda: volver_al_menu(ventanae_prod, ventanap)).pack()


# --- SUBVENTANAS VENTAS ---
# Agregar Venta
tk.Label(ventanaC_ven, text="Agregar Nueva Venta ", font=("Arial", 11, "bold")).pack(pady=5)
tk.Label(ventanaC_ven, text="Nombre del Usuario:").pack() 
entry_usuario = tk.Entry(ventanaC_ven, width=30); entry_usuario.pack(pady=2)
tk.Label(ventanaC_ven, text="Descripción:").pack()
entry_v_desc = tk.Entry(ventanaC_ven, width=30); entry_v_desc.pack(pady=2)
tk.Label(ventanaC_ven, text="Precio:").pack()
entry_v_precio = tk.Entry(ventanaC_ven, width=10); entry_v_precio.pack(pady=2)
tk.Button(ventanaC_ven, text="Guardar Venta", command=crear_venta, bg="lightgreen").pack(pady=5)
tk.Button(ventanaC_ven, text="Volver", command=lambda: volver_al_menu(ventanaC_ven, ventanav)).pack() 

# Buscar venta
tk.Label(ventanar_ven, text="Buscar Venta por ID", font=("Arial", 11, "bold")).pack(pady=5)
entry_v_id = tk.Entry(ventanar_ven, width=15); entry_v_id.pack(pady=5)
tk.Button(ventanar_ven, text="Buscar Venta", command=buscar_venta, bg="lightblue").pack(pady=5)
lbl_res_vent = tk.Label(ventanar_ven, text="Los resultados aparecerán aquí", fg="gray"); lbl_res_vent.pack(pady=5)
tk.Button(ventanar_ven, text="Volver", command=lambda: volver_al_menu(ventanar_ven, ventanav)).pack() 

# Actualizar venta
tk.Label(ventanau_ven, text="Modificar Datos de Venta", font=("Arial", 11, "bold")).pack(pady=5)
entry_mod_vid = tk.Entry(ventanau_ven, width=15); entry_mod_vid.pack(pady=5)
tk.Button(ventanau_ven, text="Cargar Datos", command=cargar_venta, bg="lightblue").pack(pady=5)
lbl_status_v = tk.Label(ventanau_ven, text="Introduce un ID y presiona 'Cargar Datos'", fg="gray"); lbl_status_v.pack(pady=5)
tk.Frame(ventanau_ven, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)
tk.Label(ventanau_ven, text="Nuevo Usuario:").pack() 
entry_mod_vnombre = tk.Entry(ventanau_ven, width=30); entry_mod_vnombre.pack(pady=2)
tk.Label(ventanau_ven, text="Nueva Descripción:").pack()
entry_mod_vdesc = tk.Entry(ventanau_ven, width=30); entry_mod_vdesc.pack(pady=2)
tk.Label(ventanau_ven, text="Nuevo Precio:").pack()
entry_mod_vprecio = tk.Entry(ventanae_ven, width=10); entry_mod_vprecio.pack(pady=2) 
tk.Button(ventanau_ven, text="Actualizar Venta", command=actualizar_venta, bg="lightgreen").pack(pady=5)
tk.Button(ventanau_ven, text="Cancelar", command=lambda: [limpiar_ventana_editar_venta(), volver_al_menu(ventanau_ven, ventanav)]).pack() 

# Eliminar Venta
tk.Label(ventanae_ven, text="Eliminar Venta por ID", font=("Arial", 11, "bold")).pack(pady=5)
entry_del_vid = tk.Entry(ventanae_ven, width=15); entry_del_vid.pack(pady=5)
tk.Button(ventanae_ven, text="Eliminar Venta", command=eliminar_venta, bg="salmon").pack(pady=5)
tk.Button(ventanae_ven, text="Volver", command=lambda: volver_al_menu(ventanae_ven, ventanav)).pack() 


# SUBVENTANA INVENTARIO 
tk.Label(ventanainv_table, text="Historial General de Ventas", font=("Arial", 12, "bold")).pack(pady=10)

#  El Frame 
frame_tabla = tk.Frame(ventanainv_table, bd=2, relief=tk.GROOVE)
frame_tabla.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

# Creamos la tabla definiendo sus columnas
columnas = ("id", "usuario", "descripcion", "precio")
tabla_ventas = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

# Definir los títulos visibles de las columnas
tabla_ventas.heading("id", text="ID Venta")
tabla_ventas.heading("usuario", text="Usuario")
tabla_ventas.heading("descripcion", text="Descripción")
tabla_ventas.heading("precio", text="Precio")

# Ajustar el espacio de cada columna (anchos y alineaciones)
tabla_ventas.column("id", width=60, anchor=tk.CENTER)
tabla_ventas.column("usuario", width=120, anchor=tk.W)
tabla_ventas.column("descripcion", width=200, anchor=tk.W)
tabla_ventas.column("precio", width=80, anchor=tk.E)

# Añadimos una barra de desplazamiento 
scroll_vertical = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla_ventas.yview)
tabla_ventas.configure(yscrollcommand=scroll_vertical.set)

# Ordenamos todo ordenadamente dentro del Frame contenedor
tabla_ventas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_vertical.pack(side=tk.RIGHT, fill=tk.Y)
tk.Button(ventanainv_table, text="Refrescar Datos", command=mostrar_ventas_inventario, bg="lightcyan", width=15).pack(pady=5)
tk.Button(ventanainv_table, text="Volver", command=lambda: volver_al_menu(ventanainv_table, ventanainv), width=15).pack(pady=10)

# botones antes de la tabla
tk.Button(ventanainv, text="Ver Tabla de Ventas", command=lambda: abrir_seccion(ventanainv_table, ventanainv), bg="lightblue", width=20).pack(pady=20)
tk.Button(ventanainv, text="actualizar datos", command=lambda: abrir_seccion(ventanau_ven, ventanainv), bg="lightcyan", width=20).pack(pady=5)
tk.Button(ventanainv, text="Volver al Inicio", command=lambda: volver_al_menu(ventanainv, ventanai), bg="salmon", width=20).pack(pady=10)
# ==================================================================
# INICIALIZACIÓN
# ==================================================================
ventanai.mainloop()

cursor.close()
conect.close()