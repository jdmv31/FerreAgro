import sqlite3
import tkinter as tk
from tkinter import messagebox
import logicabd as BDM
from tkinter import ttk

BDM.CrearTabla()


def EsDecimal(numero):
    if any (c.isalpha() for c in numero):
        return False
    
    return True


def ConfirmarRegistro(entry_nombre,entry_cant,entry_precio,ventana):
    nombre = entry_nombre.get()
    cantidad = entry_cant.get().strip()
    precio = entry_precio.get().strip().replace(",",".")
    precio = precio.replace("-","")
    cantidad = cantidad.replace("-","")

    if nombre !="" and cantidad != "" and precio != "":
        nombre = nombre.upper()
        if cantidad.isdigit() and EsDecimal(precio):
            cant = int(cantidad)
            monto = float(precio)

            if cant == 0:
                messagebox.showwarning("Cantidad Incorrecta",
                                       "La cantidad de producto disponible no puede ser nula, intente nuevamente.",
                                       parent = ventana)
            elif monto == 0:
                messagebox.showwarning("Precio Incorrecto",
                                       "El precio del producto no puede ser igual a cero, intente nuevamente.",
                                       parent = ventana)
            else:
                BDM.IngresarProducto(nombre,cant,monto)
                messagebox.showinfo("Registro Exitoso",
                                    "El producto ha sido registrado en la base de datos exitosamente"
                                    ,parent=ventana)      
        elif not cantidad.isdigit():
            messagebox.showwarning("Error en la Cantidad Disponible",
                                   "La cantidad ingresada no puede contener caracteres alfabeticos, intente nuevamente."
                                   ,parent = ventana)
        if not EsDecimal(precio):
            messagebox.showwarning("Precio Incorrecto","El precio ingresado no puede contener caracteres alfabéticos, intente nuevamente.",
                                   parent = ventana)
    else:
        messagebox.showwarning("Error en los Datos Ingresados",
                         "Alguno de los datos solicitados ha sido ingresado incorrectamente, intente nuevamente.",
                         parent=ventana)

def AgregarProducto():
    ventana = tk.Toplevel()
    ventana.title("Agregar Productos")
    ventana.geometry("1280x650")
    ventana.iconbitmap("logotipo.ico")
    frame_p = tk.Frame(ventana)
    frame_p.pack(expand=True, fill="both")
    frame_der = tk.Frame(frame_p, bg="lightgray", width=300)
    frame_der.pack(side="right", fill="y")
    frame_izq = tk.Frame(frame_p, bg="white")
    frame_izq.pack(side="left", fill="both", expand=True)

    entry_nombre = tk.Entry(frame_der)
    entry_cant = tk.Entry(frame_der)
    entry_precio = tk.Entry(frame_der)

    lbl_principal = tk.Label(frame_izq, text = "Productos Registrados",font = ("Trebuchet MS",16,"bold")
                             ,bg = "white")
    lbl_principal.pack(side = tk.TOP, pady = 20)

    lbl_nombre = tk.Label(frame_der,text = "Ingrese el nombre del Producto", font=("Trebuchet MS",16,"bold"),
                          bg = "lightgray")
    lbl_nombre.pack(pady = 5)
    entry_nombre.pack(pady = 5)

    lbl_cant = tk.Label(frame_der,text = "Ingrese la cantidad existente del Producto",font = ("Trebuchet MS",16,"bold"),
                        bg = "lightgray")
    lbl_cant.pack(pady = 5)
    entry_cant.pack(pady = 5)

    lbl_precio = tk.Label(frame_der,text = "Ingrese el precio del Producto", font = ("Trebuchet MS",16,"bold"),
                          bg = "lightgray")
    lbl_precio.pack(pady = 5)
    entry_precio.pack(pady = 5)

    btn_confirmar = tk.Button(frame_der,text = "Confirmar Registro", width = 20, height = 2,
                              command= lambda: (ConfirmarRegistro(entry_nombre,entry_cant,entry_precio,ventana)))
    btn_confirmar.pack(pady = 15)

    lista = ttk.Treeview(frame_izq, columns=("id", "nombre", "cantidad", "precio"), show="headings")
    lista.heading("id", text="ID")
    lista.heading("nombre", text="Nombre")
    lista.heading("cantidad", text="Cantidad")
    lista.heading("precio", text="Precio")
    lista.column("id", width=50)
    lista.column("nombre", width=200)
    lista.column("cantidad", width=100, anchor="center")
    lista.column("precio", width=100, anchor="center")
    lista.pack(fill="both", expand=True, padx=20, pady=10)
    lista.pack(fill="both",expand = True)
        
    frame_secundario = tk.Frame(frame_der,bg = "gray")
    frame_secundario.pack(side="bottom",pady = 40, fill="x")

    btn_actualizar = tk.Button(frame_secundario, text = "Actualizar Tabla",width = 20, height = 2,
                               command= lambda: (BDM.CargarProductos(lista)))
    btn_actualizar.pack(expand = True,pady = 20)


    btn_volver = tk.Button(frame_secundario,text = "Volver al Menu Principal", width = 30, height = 2,
                            bg = "red", command = lambda: (CerrarVentana(ventana)),fg = "white")
    btn_volver.pack (side = tk.BOTTOM, expand = True,pady = 20)
    if not BDM.TablaVacia():
        BDM.CargarProductos(lista)

    centrar_ventana(ventana,1280,650)
    ventana.resizable(False,False)


def CerrarVentana(vent):
    vent.destroy()

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

root = tk.Tk()
root.title("Gestion de Inventario")
root.iconbitmap("logotipo.ico") 


label_titulo = tk.Label(root, text="Gestión de Inventario", font=("Trebuchet MS", 40, "bold"))
label_titulo.pack(pady=20)


frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

btn_agregar = tk.Button(frame_botones, text="Agregar Producto", 
                        command=AgregarProducto, width=20, height=2)
btn_agregar.pack(pady=5)

btn_ver = tk.Button(frame_botones, text="Inventario Disponible", 
                     width=20, height=2)
btn_ver.pack(pady=5)

btn_registrar = tk.Button(frame_botones, text = "Registrar Ventas", width = 20,height = 2)
btn_registrar.pack(pady = 5)

btn_salir = tk.Button(root, text="Salir del Programa",command = lambda: (CerrarVentana(root)),
                      width=20, bg="red", fg="white")
btn_salir.pack(pady=15)

centrar_ventana(root,600,480)
root.minsize(600,480)
root.resizable(False,False)

root.mainloop()