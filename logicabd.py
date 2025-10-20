import sqlite3
import tkinter as tk
from tkinter import messagebox

def Conectar():
    return sqlite3.connect("inventario.db")

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

def ObtenerProductos():
    conn = Conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id,nombre,cantidad,precio FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def CargarProductos(lista):
    lista.delete(*lista.get_children())
    if TablaVacia():
        messagebox.showinfo("No se encontraron Productos",
                            "Actualmente no se encuentran productos disponibles en inventario."
                            ,parent = lista)
    productos = ObtenerProductos()
    for producto in productos:
        lista.insert("","end",values = producto)