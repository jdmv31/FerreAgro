import sqlite3
import tkinter as tk
from tkinter import messagebox
import logicabd as BDM
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Treeview
from ttkbootstrap.constants import *
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

BDM.CrearTabla()
BDM.CrearTablaVentas()


def ContieneLetras(numero):
    if any (c.isalpha() for c in numero):
        return False
    
    return True


def ConfirmarRegistro(entry_nombre,entry_cant,entry_precio,ventana):
    nombre = entry_nombre.get()
    cantidad = entry_cant.get().strip().replace(",","").replace("-","").replace(".","")
    precio = entry_precio.get().strip().replace(",","").replace("-","").replace(".","")

    if nombre !="" and cantidad != "" and precio != "":
        nombre = nombre.upper()
        if cantidad.isdigit():
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
        if not ContieneLetras(precio):
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

    lbl_precio = tk.Label(frame_der,text = "Ingrese el precio del Producto en dólares", font = ("Trebuchet MS",16,"bold"),
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
    lista.heading("precio", text="Precio ($)")
    lista.column("id", width=50)
    lista.column("nombre", width=200)
    lista.column("cantidad", width=100, anchor="center")
    lista.column("precio", width=100, anchor="center")
    lista.pack(fill="both", expand=True, padx=20, pady=10)
    lista.pack(fill="both",expand = True)
        
    frame_secundario = tk.Frame(frame_der,bg = "gray")
    frame_secundario.pack(side="bottom",pady = 40, fill="x")

    btn_actualizar = tk.Button(frame_secundario, text = "Actualizar Tabla",width = 20, height = 2,
                               command= lambda: (BDM.CargarProductos(lista,0)))
    btn_actualizar.pack(expand = True,pady = 20)


    btn_volver = tk.Button(frame_secundario,text = "Volver al Menu Principal", width = 30, height = 2,
                            bg = "red", command = lambda: (CerrarVentana(ventana)),fg = "white")
    btn_volver.pack (side = tk.BOTTOM, expand = True,pady = 20)
    if not BDM.TablaVacia():
        BDM.CargarProductos(lista,0)

    CentrarVentana(ventana,1280,650)
    ventana.resizable(False,False)

def Modificacion(entry_cantidad, entry_precio, datos,modal):
    try:
        cant_str = entry_cantidad.get().strip().replace("-", "").replace(",", "").replace(".","")
        precio_str = entry_precio.get().strip().replace("-", "").replace(",", "").replace(".","")
        cant = int(cant_str)
        precio = float(precio_str)

        if cant < int(datos[2]):
            messagebox.showwarning("Error", "La cantidad a modificar no puede ser menor a la establecida.",
                                   parent=modal)
        elif cant == 0 or precio == 0:
            messagebox.showwarning("Error", "La cantidad o el precio a modificar no puede ser nulo.\nIntente nuevamente."
                                   ,parent=modal)
        else:
            BDM.ActualizarBD(datos[0], cant, precio)
            messagebox.showinfo("Modificacion Exitosa", 
                                "Se han modificado correctamente los datos asignados."
                                ,parent=modal)            
            CerrarVentana(modal)


    except ValueError:
        messagebox.showwarning("Error", "La cantidad o el precio a modificar deben ser valores numéricos.\nIntente nuevamente.",
                               parent=modal)

def ModificarProducto(datos):
    modal = ttk.Toplevel(vent_mod)
    modal.title(f"Modificar {datos[1]}")
    modal.geometry("400x250")
    modal.position_center()
    modal.resizable(False, False)
    modal.grab_set()
    modal.iconbitmap("logotipo.ico")

    ttk.Label(modal, text="Cantidad:", font=("Segoe UI", 11)).pack(pady=(20, 5))
    entry_cantidad = ttk.Entry(modal)
    entry_cantidad.insert(0, datos[2])
    entry_cantidad.pack()

    ttk.Label(modal, text="Precio ($):", font=("Segoe UI", 11)).pack(pady=(15, 5))
    entry_precio = ttk.Entry(modal)
    entry_precio.insert(0, datos[3])
    entry_precio.pack()
    boton = ttk.Button(modal,
                       text="Guardar",
                       bootstyle=SUCCESS,
                       command=lambda: Modificacion(entry_cantidad, entry_precio, datos,modal))
    boton.pack(pady=15)

def SeleccionarProducto(event):
    item = lista.focus()
    if item:
        valores = lista.item(item, "values")
        respuesta = messagebox.askyesno(
            "Modificar producto",
            f"¿Deseas modificar el producto '{valores[1]}'?\nPuedes cambiar la cantidad o el precio.",
            parent = vent_mod
        )
        if respuesta:
            ModificarProducto(valores)

def ModificarMercancia():
    if BDM.TablaVacia():
        messagebox.showwarning("Error", "No se encuentran productos registrados en la base de datos, agregue productos antes de modificarlos.")
        return
    else:
        global vent_mod
        vent_mod = ttk.Window(
            title="Modificar Productos",
            size=(1280, 650),
            position=(100, 100)
        )
        vent_mod.iconbitmap("logotipo.ico")
        label_principal = ttk.Label(
            vent_mod,
            text="Productos Disponibles",
            font=("Trebuchet MS", 24, "bold")
        )
        label_principal.pack()

        frame = ttk.Frame(vent_mod)
        frame.pack(fill="both", expand=True)

        global lista
        lista = ttk.Treeview(
            frame,
            columns=("id", "nombre", "cantidad", "precio"),
            show="headings"
        )
        lista.heading("id", text="ID")
        lista.heading("nombre", text="Nombre")
        lista.heading("cantidad", text="Cantidad")
        lista.heading("precio", text="Precio ($)")
        lista.column("id", width=50)
        lista.column("nombre", width=200)
        lista.column("cantidad", width=100, anchor="center")
        lista.column("precio", width=100, anchor="center")
        lista.pack(fill="both", expand=True, padx=15, pady=20)
        lista.bind("<Double-1>",SeleccionarProducto)
        boton_volver = ttk.Button(vent_mod,
                                  text="Volver al Menu Principal",
                                  command=lambda:CerrarVentana(vent_mod),
                                  bootstyle=DANGER)
        boton_volver.pack(pady=15)
        BDM.CargarProductos(lista, 0)
        vent_mod.resizable(False, False)
        CentrarVentana(vent_mod, 1280, 650)

def GuardarVenta (entry, datos, modal):
    try:
        cant_str = entry.get().strip().replace("-", "").replace(",", "").replace(".","")
        cant = int(cant_str)

        if cant > int(datos[2]):
            messagebox.showwarning("Error", "La cantidad a vender no puede ser mayor a la existente.",
                                   parent=modal)
        elif cant == 0:
            messagebox.showwarning("Error", "La cantidad a vender no puede ser nula.\nIntente nuevamente."
                                   ,parent=modal)
        else:
            if cant == int(datos[2]):
                messagebox.showinfo("Se ha agotado el producto",
                                    "Se ha vendido la totalidad de la mercancia, debe reabastecer el producto y registarlo en el sistema.")
            nueva_cant = int(datos[2]) - cant
            totalidad = cant * float(datos[3])
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            BDM.ActualizarBD(datos[0],nueva_cant,datos[3])
            BDM.IngresarVenta(datos[0],cant,totalidad,fecha)
            messagebox.showinfo("Venta Registrada Exitosamente", 
                                "Se ha registrado correctamente la venta, se ha actualizado la base de datos."
                                ,parent=modal)            
            CerrarVentana(modal)


    except ValueError:
        messagebox.showwarning("Error", "La cantidad vendida debe contener valores numéricos.\nIntente nuevamente.",
                               parent=modal)

def Venta(datos):
    modal = ttk.Toplevel(vent_venta)
    modal.geometry("400x250")
    modal.title("Registrar Venta")
    modal.position_center()
    modal.resizable(False, False)
    modal.grab_set()
    modal.iconbitmap("logotipo.ico")
    ttk.Label(modal, text="Cantidad Vendida: ", font=("Segoe UI", 11)).pack(pady=(15,5))
    entry = ttk.Entry(modal)
    entry.insert(0,datos[2])
    entry.pack()
    boton = ttk.Button(modal,
                       text="Registrar Venta",
                       bootstyle=SUCCESS,
                       command=lambda:GuardarVenta(entry,datos,modal))
    boton.pack(pady=15)

def VentaProducto(event):
    item = lista.focus()
    if item:
        valores = lista.item(item,"values")
        respuesta = messagebox.askyesno(
            "Realizar Venta",
            f"¿Deseas registrar una venta del producto '{valores[1]}'?",
            parent = vent_venta
        )
        if respuesta:
            Venta(valores)


def RegistrarVenta():
    if BDM.TablaVacia():
        messagebox.showwarning("Error", "No se encuentran productos registrados en la base de datos, agregue productos antes de poder registrar una venta.")
        return
    else:
        global vent_venta
        vent_venta = ttk.Window(title="Registra Ventas",
                                size=(1280,650),
                                position=(100,100))
        vent_venta.iconbitmap("logotipo.ico")
        frame1 = ttk.Frame(vent_venta)
        frame1.pack(fill="both",expand=True)
        titulo = ttk.Label(frame1,
                           text="Registrar Ventas",
                           font=("Trebuchet MS",24,"bold"))
        titulo.pack(pady=15)
        global lista
        lista = ttk.Treeview(
            frame1,
            columns=("id", "nombre", "cantidad", "precio"),
            show="headings"
        )
        lista.heading("id", text="ID")
        lista.heading("nombre", text="Nombre")
        lista.heading("cantidad", text="Cantidad")
        lista.heading("precio", text="Precio ($)")
        lista.column("id", width=50)
        lista.column("nombre", width=200)
        lista.column("cantidad", width=100, anchor="center")
        lista.column("precio", width=100, anchor="center")
        lista.pack(fill="both", expand=True, padx=15, pady=20)
        lista.bind("<Double-1>",VentaProducto)
        boton_volver = ttk.Button(vent_venta,
                                  text="Volver al Menu Principal",
                                  command=lambda:CerrarVentana(vent_venta),
                                  bootstyle=DANGER)
        boton_volver.pack(pady=15)

        BDM.CargarProductos(lista, 0)
        CentrarVentana(vent_venta,1280,650)
        vent_venta.resizable(False,False)


def CerrarVentana(vent):
    vent.destroy()

def CentrarVentana(ventana, ancho, alto):
    ventana.update_idletasks()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

root = ttk.Window(title="Gestion de Inventario FerreAgro", themename="darkly")
root.state("zoomed")
root.iconbitmap("logotipo.ico")

style = ttk.Style()
style.configure("Fondo.TFrame", background="#0d0a1c")
style.configure("Frame.TFrame", background="#201a47")
style.configure("Titulo.TLabel", background="#0d0a1c", foreground="white")
style.configure("Aviso.TLabel",background="#201a47", foreground="white")

fondo = ttk.Frame(root, style="Fondo.TFrame")
fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

titulo = ttk.Label(fondo,
                   text="Gestion de Inventario Materiales FerreAgro",
                   font=("Trebuchet MS", 24, "bold"),
                   style="Titulo.TLabel")
titulo.pack(pady=20)

frame = ttk.Frame(fondo, padding=(20, 10), style="Fondo.TFrame")
frame.pack(fill="both", expand=True)

frame_izq = ttk.LabelFrame(frame,
                           style="Frame.TFrame",
                           width=250,
                           padding=10)
frame_izq.pack(side="left", fill="y", padx=10, pady=10)
frame_izq.pack_propagate(False)

frame_der = ttk.Label(frame,style="Frame.TFrame")
frame_der.pack(side="right",fill="both",padx=10,pady=10, expand = True)

subframe_izq = ttk.Frame(frame_der,style="Frame.TFrame")
subframe_izq.pack(side="left",fill="both",expand=True)
subframe_der = ttk.Frame(frame_der,style="Frame.TFrame")
subframe_der.pack(side="left",fill="both",expand=True)

if BDM.TablaVacia():
    aviso = ttk.Label(subframe_izq,text="No hay productos registrados en el sistema.",
                      font=("Trebuchet MS",15,"bold"),
                      style="Aviso.TLabel")
    aviso.pack(pady = 20)
else:
    titulo = ttk.Label(subframe_izq,
                       text="Productos Disponibles",style="Aviso.TLabel",
                       font=("Trebuchet MS",15,"bold"))
    titulo.pack()
    lista = ttk.Treeview(subframe_izq,columns=("id","nombre","cantidad","precio","totalidad"),show="headings")
    lista.heading("id", text="ID")
    lista.heading("nombre",text="Nombre")
    lista.heading("cantidad",text="Cantidad")
    lista.heading("precio",text="Precio ($)")
    lista.heading("totalidad",text="Totalidad ($)")
    lista.column("id",width ="50")
    lista.column("nombre",width="200")
    lista.column("cantidad",width="100",anchor="center")
    lista.column("precio",width="100",anchor="center")
    lista.column("totalidad",width="100",anchor="center")
    lista.pack(fill="both",expand = True,padx=15,pady=20)
    lista.pack(fill="both",expand=True)
    BDM.CargarProductos(lista,1)


if BDM.TablaVaciaVentas():
    aviso = ttk.Label(subframe_der,
                      text="No hay ventas registradas en el sistema.",
                      font=("Trebuchet MS", 15, "bold"),
                      style="Aviso.TLabel")
    aviso.pack(pady=20)
else:
    datos = BDM.MasVendidos()

    nombres = [item[0] for item in datos]
    cantidades = [item[1] for item in datos]

    COLOR_FONDO = '#2F2F2F'
    COLOR_TEXTO = 'white'
    COLOR_BORDE_GRAFICO = '#373737'

    fig = Figure(figsize=(4, 4), dpi=100, facecolor=COLOR_FONDO)
    ax = fig.add_subplot(111)
    ax.set_facecolor(COLOR_FONDO)

    ax.set_title("Productos más vendidos", color=COLOR_TEXTO)

    wedges, texts, autotexts = ax.pie(
        cantidades, 
        labels=nombres, 
        autopct="%1.1f%%", 
        startangle=140,
        textprops={'color': COLOR_TEXTO},
        wedgeprops={'edgecolor': COLOR_BORDE_GRAFICO}
    )

    for autotext in autotexts:
        autotext.set_color(COLOR_TEXTO)


    canvas = FigureCanvasTkAgg(fig, master=subframe_der)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

btn_agregar = ttk.Button(frame_izq,
                         text="Agregar Producto",
                         command=AgregarProducto,
                         bootstyle="success-outline",
                         padding=(30, 15))
btn_agregar.pack(pady=10)

btn_registrar = ttk.Button(frame_izq,
                           text="Registrar Ventas",
                           command=RegistrarVenta,
                           bootstyle="success-outline",
                           padding=(35, 15))
btn_registrar.pack(pady=10)

btn_actualizar = ttk.Button(frame_izq,
                            text="Modificar Mercancia",
                            command=ModificarMercancia,
                            bootstyle="success-outline",
                            padding=(25, 15))
btn_actualizar.pack(pady=10)

btn_salir = ttk.Button(frame_izq,
                       text="Salir del Programa",
                       command=lambda: CerrarVentana(root),
                       bootstyle="danger-outline",
                       padding=(30, 15))
btn_salir.pack(pady=15, side="bottom")

root.minsize(600, 480)
root.mainloop()