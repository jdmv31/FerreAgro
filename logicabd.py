import sqlite3
import tkinter as tk
from tkinter import messagebox

def Conectar():
    return sqlite3.connect("inventario.db")

def ConectarVentas():
    return sqlite3.connect("ventas.db")

def CrearTabla():
    conn = Conectar()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def CrearTablaVentas():
    conn = ConectarVentas()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                totalidad REAL NOT NULL,
                fecha TEXT NOT NULL -- formato: 'YYYY-MM-DD HH:MM:SS'
            )
    """)
    conn.commit()
    conn.close()

def IngresarVenta(nombre,cantidad,totalidad,fecha):
    conn = ConectarVentas()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ventas (producto,cantidad,totalidad,fecha) VALUES (?,?,?,?)",
                   (nombre,cantidad,totalidad,fecha))
    conn.commit()
    conn.close()


def IngresarProducto(nombre,cantidad,precio):
    conn = Conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre,cantidad,precio) VALUES (?,?,?)",
                   (nombre,cantidad,precio))
    conn.commit()
    conn.close()

def TablaVacia():
    conn = Conectar()
    cursor = conn.cursor()
    cursor.execute (f"SELECT COUNT (*) FROM productos")
    cant = cursor.fetchone()[0]
    conn.close()
    return cant == 0

def TablaVaciaVentas():
    conn = ConectarVentas()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT (*) FROM ventas")
    cant = cursor.fetchone()[0]
    conn.close()
    return cant == 0

def ObtenerProductos():
    conn = Conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id,nombre,cantidad,precio FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def CargarProductos(lista,arg):
    lista.delete(*lista.get_children())
    if TablaVacia():
        messagebox.showinfo("No se encontraron Productos",
                            "Actualmente no se encuentran productos disponibles en inventario."
                            ,parent = lista)
        return
    productos = ObtenerProductos()
    for producto in productos:
        if arg == 1:
            id_,nombre,cantidad,precio = producto
            total = float(cantidad * precio)
            fila = (id_,nombre,cantidad,precio,round(total,2))
            lista.insert("","end",values = fila)
        else:
            lista.insert("","end",values = producto)

def ActualizarBD(id, cantidad, precio):
    conn = Conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET precio = ?, cantidad = ? WHERE id = ?",
                    (precio, cantidad, id))
    conn.commit()
    conn.close()

def MasVendidos(limite=10):
    conn = ConectarVentas()
    cursor = conn.cursor()
    
    try:
        cursor.execute("ATTACH DATABASE 'inventario.db' AS inv")
        query = """
            SELECT 
                p.nombre,  -- p.nombre viene de la BD 'inv'
                SUM(v.cantidad) AS total_vendido
            FROM 
                ventas AS v          -- 'ventas' es de la BD principal
            JOIN 
                inv.productos AS p ON v.producto = p.id -- Cruzamos con inv.productos
            GROUP BY 
                p.nombre
            ORDER BY 
                total_vendido DESC
            LIMIT ?
        """
        
        cursor.execute(query, (limite,))
        resultados = cursor.fetchall()
        cursor.execute("DETACH DATABASE 'inv'")
        
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        resultados = []
    finally:
        conn.close()
    return resultados