from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import sqlite3
from tkinter.font import BOLD
from tkcalendar import DateEntry

class App:
     
    def crearusers(self):
        conn = sqlite3.connect('sensorial.db')
        """
        Crea la tabla 'users' en la base de datos 'sensorial.db' si no existe,
        y luego inserta un usuario de ejemplo ('admin', 'sensor2023').
        """
        cursor = conn.cursor()

        create_users_table_sql = '''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL,
                                    password TEXT NOT NULL);
                                '''
        cursor.execute(create_users_table_sql)

        conn.commit()

        insert_users_data_sql = '''INSERT INTO IF NOT EXISTS users (username, password) VALUES (?, ?);'''
        data_to_insert_users = ('admin', 'sensor2023')
        cursor.execute(insert_users_data_sql, data_to_insert_users)

        conn.commit()
        
        conn.close()
    
    def verificar_entradas(self):
        """
        Verifica si los campos de usuario y contraseña están llenos.
        Si están vacíos, muestra un mensaje de error, de lo contrario, llama a la función verificar.
        """
        contenido_usuario = self.usuario.get()
        contenido_password = self.password.get()

        if not contenido_usuario or not contenido_password:
            messagebox.showerror(message="Por favor, llena ambos campos.", title="Mensaje")
            self.limpiarCampos()
        else:
            self.verificar()
    
    def funcEnter(self):
        """
        Establece el foco en el campo de contraseña cuando se presiona la tecla Enter en el campo de usuario.
        """
        self.password.focus_set()
    
    def limpiarCampos(self):
        """
        Limpia los campos de entrada de usuario y contraseña.
        """
        self.usuario.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.usuario.focus_set() 
    
    def verificar(self):
        """
        Verifica el inicio de sesión comparando el usuario y la contraseña ingresados
        con los datos almacenados en la base de datos 'sensorial.db'.
        """
        usuario = self.usuario.get()
        password = self.password.get()
        
        conn = sqlite3.connect('sensorial.db')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        row = cursor.fetchone()

        if row is not None and usuario == row[1] and password == row[2]:
            query = "UPDATE users SET activo=1 WHERE id=1;"
            cursor.execute(query)
            messagebox.showinfo(message="INICIO DE SESIÓN EXITOSO", title="Mensaje")
            print(f"SESIÓN INICIADA")
            conn.commit()
            cursor.close()
            conn.close()
            
            self.ventana.destroy()
            Menu()
            
        else:
            messagebox.showerror(message="Usuario o contraseña inválidos.", title="Mensaje")
            self.limpiarCampos()
    
    # Constructor de la clase
    def __init__(self):
        
        # Llama al método para crear la tabla de usuarios
        self.crearusers
        
        # Creación de la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de Sesión')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        
        # Cálculos para centrar la ventana en la pantalla
        pantall_ancho = self.ventana.winfo_screenwidth()
        pantall_largo = self.ventana.winfo_screenheight()
        x = int((pantall_ancho/2) - (800/2))
        y = int((pantall_largo/2) - (500/2))
        self.ventana.geometry(f'800x500+{x}+{y}')
        
        # Carga y redimensiona la imagen del logo
        logo = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/sensorial.png").resize((300,280), Image.Resampling.LANCZOS))
        
        # Creación de un marco y etiqueta para mostrar el logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=350, relief=tk.SOLID, padx=10, pady=10, bg='#F8E9E2')
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#F8E9E2')
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Creación de un marco para el formulario de inicio de sesión
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        
        # Creación de un encabezado con el título "Inicio de Sesión"
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de Sesión",font=('Comic Sans MS', 38, "bold"), fg='black', bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        
        # Creación de un marco para el formulario de inicio de sesión
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side='bottom', expand=tk.YES, fill=tk.BOTH)
        
        # Creación de etiquetas y campos de entrada para usuario y contraseña
        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario*", font=('Comic Sans MS', 15), fg='black', bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Comic Sans MS', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)
        self.usuario.bind("<Return>", lambda event=None: self.funcEnter())
        
        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña*", font=('Comic Sans MS', 15), fg='black', bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Comic Sans MS', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")
        self.password.bind("<Return>",lambda event=None: self.verificar_entradas())
        
        # Creación de un botón para iniciar sesión
        inicio = tk.Button(frame_form_fill, text="Iniciar Sesión", font=('Comic Sans MS', 15, BOLD), bg='#febda7', bd=4, fg="black", command=self.verificar_entradas)
        inicio.pack(fill=tk.X, padx=110, pady=30)
        usuario = self.usuario.get()
        password = self.password.get()
        inicio.bind("<Return>", lambda event=None: self.verificar(usuario, password))
        
        # Limpia los campos de entrada
        self.limpiarCampos()
        
        self.ventana.mainloop()

class Menu:
    
    # Redirige a la pantalla de Inventario de productos
    def dirigir_inventario(self):
        self.ventana.destroy()
        Inventario1()
    
    # Redirige a la pantalla de Ventas
    def dirigir_ventas(self):
        self.ventana.destroy()
        Ventas()
    
    # Maneja la acción de salir de la aplicación
    def salir(self):
        
        conn = sqlite3.connect('sensorial.db')

        cursor = conn.cursor()
        
        respuesta = messagebox.askyesno("ADVERTENCIA","¿Seguro que deseas cerrar la sesión?")
        if respuesta:
            # Actualiza el estado del usuario a "inactivo" en la base de datos
            query = "UPDATE users SET activo=0 WHERE id=1;"
            cursor.execute(query)
            
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(message="CIERRE DE SESIÓN EXISTOSO",title="Mensaje")
            print("SESIÓN CERRADA")
            self.ventana.destroy()
            App()
            self.ventana.destroy()
            Ventas()
        
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Menú')
        self.ventana.config(bg='#F8E9E2')
        self.ventana.resizable(width=0, height=0)
        
        # Configuración de dimensiones y posición de la ventana# Configuración de dimensiones y posición de la ventana
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
        x = int((w/2) - (800/2))
        y = int((h/2) - (500/2))
        self.ventana.geometry(f'800x500+{x}+{y}')
        
        # Configuración del menú en la parte superior de la ventana
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu = menubar)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones",menu=filemenu)
        filemenu.add_command(label="Salir",command=self.salir)
        
        # Creación del encabezado del menú
        frame_top = tk.Frame(self.ventana, bg="#fcfcfc", bd=0, width=self.ventana.winfo_reqwidth(), height=70)
        frame_top.pack(side="top", fill="both")
        titulo = tk.Label(frame_top, text="Sensorial Store: Menú", bg="#fcfcfc", font=('Comic Sans MS', 45, BOLD))
        titulo.pack()
        
        # Creación de botones para dirigir a Inventario y Ventas
        subframe_izquierdo = tk.Frame(self.ventana, bg="#faf0ef", bd=5, width=self.ventana.winfo_reqwidth() // 2)
        subframe_izquierdo.pack(side="left", fill="both", expand=True)
        boton_izquierdo = tk.Button(subframe_izquierdo, text="Inventarios", bg="#f8c8b4", width=10, height=2, bd=5, font=('Comic Sans MS', 28, BOLD), command=lambda: self.dirigir_inventario())
        boton_izquierdo.pack(expand=True)
        
        subframe_derecho = tk.Frame(self.ventana, bg="#f2f8ec", bd=5, width=self.ventana.winfo_reqwidth() // 2)
        subframe_derecho.pack(side="right", fill="both", expand=True)
        boton_derecho = tk.Button(subframe_derecho, text="Ventas", bg="#c5d1bb", width=10, height=2, bd=5, font=('Comic Sans MS', 28, BOLD), command=lambda: self.dirigir_ventas())
        boton_derecho.pack(expand=True)
        
        self.ventana.mainloop()

class Inventario1:
    
    db_name='sensorial.db'
    
    # Función para validar si un valor es numérico
    def validar_es_numero(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    # Función para deseleccionar un registro y limpiar los campos del formulario
    def deseleccionar_registro(self, event=None):
        if event and event.widget == self.ventana:
            self.tree.selection_remove(self.tree.selection())
            self.nuevo()
    
    # Función para cargar los datos de un registro seleccionado en el formulario
    def cargar_datos_seleccionados(self,event):
        
        self.tree.focus_set()
        if self.tree.selection():
            item = self.tree.selection()[0]
            valores = self.tree.item(item, 'values')
            codigo = self.tree.item(item, 'text')
            print(valores)

            self.codigo.delete(0, tk.END)
            self.combo_categoria.set("")
            self.marca.delete(0, tk.END)
            self.descripcion.delete(0, tk.END)
            self.precio_compra.delete(0, tk.END)
            self.precio_venta.delete(0, tk.END)
            self.existencias.delete(0, tk.END)
            
            self.codigo.insert(0, codigo)
            if len(valores) > 0:
                self.combo_categoria.set(valores[0])
            if len(valores) > 1:
                self.marca.insert(0, valores[1])
            if len(valores) > 2:
                self.descripcion.insert(0, valores[2])
            if len(valores) > 3:
                self.precio_compra.insert(0, valores[3])
            if len(valores) > 4:
                self.precio_venta.insert(0, valores[4])
            if len(valores) > 5:
                self.existencias.insert(0, valores[5])
    
    # Función para validar si hay un registro seleccionado        
    def validar_registro_seleccionado(self):
        selected_item = self.tree.selection()
            
        if not selected_item:
            messagebox.showerror("ERROR", "Por favor, selecciona un registro.")
            return False
        else:
            return True
    
    # Función para validar si todos los campos del formulario están completos       
    def validar_formulario_completo(self):
        if len(self.combo_categoria.get()) !=0 and len(self.marca.get()) !=0 and len(self.descripcion.get()) !=0 and len(self.precio_compra.get()) !=0 and len(self.precio_venta.get()) !=0 and len(self.existencias.get()) !=0:
            return True
        else:
             messagebox.showerror("ERROR", "Por favor, completa todos los campos del formulario.")
    
    # Función para ejecutar consultas SQL en la base de dato
    def ejecutar_consulta(self, query, parameters=()):
        try:
            with sqlite3.connect(self.db_name) as conexion:
                cursor=conexion.cursor()
                result=cursor.execute(query,parameters)
                conexion.commit()
                print("Conexión exitosa.")
            return result
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
    
    # Función para eliminar un registro       
    def delete(self):
        if self.validar_registro_seleccionado():
                selected_item = self.tree.selection()
                descripcion = self.descripcion.get()
                codigo_producto = int(self.tree.item(selected_item)['text'])
                respuesta = messagebox.askyesno("ADVERTENCIA", f"¿Seguro que deseas eliminar el producto: {self.descripcion.get()}?")
                if respuesta:
                    query = "UPDATE inventario1 SET activo=?, eliminado=? WHERE codigo=?"
                    parameters = (0, 1, codigo_producto)
                    self.ejecutar_consulta(query, parameters)

                    messagebox.showinfo("ELIMINACIÓN EXITOSA", f'Producto eliminado: {descripcion}')
                    print(f"ELIMINADO")
                    self.read()
                    self.nuevo()
    
    # Función para actualizar un registro       
    def update(self):
        if self.validar_registro_seleccionado():
            if self.validar_formulario_completo():
                if self.validar_es_numero(self.precio_compra.get()) and self.validar_es_numero(self.precio_venta.get()) and self.validar_es_numero(self.existencias.get()):
                     
                    codigo_producto = int(self.codigo.get())
                    query = 'UPDATE inventario1 SET categoria=?, marca=?, descripcion=?, precio_compra=?, precio_venta=?, existencias=? WHERE codigo=?'
                    parameters = (
                        self.combo_categoria.get(),
                        self.marca.get(),
                        self.descripcion.get(),
                        float(self.precio_compra.get()),
                        float(self.precio_venta.get()),
                        int(self.existencias.get()),
                        codigo_producto
                    )
                    self.ejecutar_consulta(query, parameters)
                    messagebox.showinfo("ACTUALIZACIÓN EXITOSA.", f'Producto actualizado: {self.descripcion.get()}')
                    print('ACTUALIZADO')
                    self.read()
                    self.nuevo()
                    
                else:
                    messagebox.showerror("ERROR", "Por favor, ingresa valores numéricos en los campos correspondientes.")    
                    
    # Función para leer los registros de la base de datos y actualizar la vista        
    def read(self):
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        query='SELECT codigo, categoria, marca, descripcion, precio_compra, precio_venta, existencias FROM inventario1 WHERE activo=1 AND eliminado=0 ORDER BY codigo DESC'
        db_rows=self.ejecutar_consulta(query)
        
        for row in db_rows:
            self.tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6]))
    
    # Función para crear un nuevo registro
    def create(self):
        if self.validar_formulario_completo():
            if self.validar_es_numero(self.precio_compra.get()) and self.validar_es_numero(self.precio_venta.get()) and self.validar_es_numero(self.existencias.get()):
                
                query_last_inactive_code = 'SELECT MAX(codigo) FROM inventario1 WHERE activo=0 AND eliminado=1'
                result = self.ejecutar_consulta(query_last_inactive_code)
                last_inactive_code = result.fetchone()[0]

                if last_inactive_code is not None:
                    new_code = last_inactive_code
                    query_update_code = 'UPDATE inventario1 SET activo=?, eliminado=? WHERE codigo=?'
                    parameters_update_code = (1, 0, last_inactive_code)
                    self.ejecutar_consulta(query_update_code, parameters_update_code)
                    
                else:
                    query_last_code = 'SELECT MAX(codigo) FROM inventario1'
                    result = self.ejecutar_consulta(query_last_code)
                    last_code = result.fetchone()[0] or 0
                    new_code = last_code + 1

                query = 'INSERT INTO inventario1 (codigo, categoria, marca, descripcion, precio_compra, precio_venta, existencias, activo, eliminado) VALUES(?,?,?,?,?,?,?,?,?)'
                parameters = (new_code, self.combo_categoria.get(), self.marca.get(), self.descripcion.get(), float(self.precio_compra.get()), float(self.precio_venta.get()), int(self.existencias.get()), 1, 0)
                self.ejecutar_consulta(query, parameters)

                messagebox.showinfo("REGISTRO EXITOSO.", f'Producto registrado: {self.descripcion.get()}')
                print('REGISTRADO')
                self.read()
                self.nuevo()
                
            else:
                messagebox.showerror("ERROR", "Por favor, ingresa valores numéricos en los campos correspondientes.")
                
    # Función para limpiar el formulario y prepararlo para un nuevo registro        
    def nuevo(self):
        self.codigo.delete(0, tk.END)
        self.combo_categoria.set("")
        self.combo_categoria.set(self.combo_categoria["values"][0])
        self.marca.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)
        self.precio_compra.delete(0, tk.END)
        self.precio_venta.delete(0, tk.END)
        self.existencias.delete(0, tk.END)
        self.existencias.insert(0, "0")
        self.codigo.focus_set()
        self.deseleccionar_registro()
    
    # Funciones para incrementar y decrementar la cantidad de existencias        
    def decrementar(self):
        valor_actual = tk.IntVar()
        
        valor_actual = (self.numero.get())
        
        if valor_actual > 0:
            nuevo_valor = valor_actual - 1
            self.numero.set(int(nuevo_valor))
            self.existencias.icursor(len(str(nuevo_valor)))
    
    def incrementar(self):
        
        valor_actual = (self.numero.get())
        
        if valor_actual < 50:
        
            nuevo_valor = valor_actual + 1
            self.numero.set(int(nuevo_valor))
            self.existencias.icursor(len(str(nuevo_valor)))
    
    # Funciones para cambiar entre los diferentes inventarios
    def abrir_inventario1(self):
        
        self.ventana.destroy()
        Inventario1()
    
    def abrir_inventario2(self):
        
        self.ventana.destroy()
        Inventario2()
    
    # Funciones para navegar atrás o salir de la aplicación   
    def atras(self):
        
        self.ventana.destroy()
        Menu()
        
    def salir(self):
        
        respuesta = messagebox.askyesno("ADVERTENCIA","¿Seguro que deseas cerrar la sesión?")
        if respuesta:
        
            query = "UPDATE users SET activo=0 WHERE id=1;"
            self.ejecutar_consulta(query)

            messagebox.showinfo(message="CIERRE DE SESIÓN EXISTOSO",title="Mensaje")
            print("SESIÓN CERRADA")
            self.ventana.destroy()
            App()

    def __init__(self):
        
        # Función para crear un espacio vertical
        def espacio_vertical(self):
            espacio_vertical = tk.Frame(self.ventana, height=20, bg="#faf0ef")
            espacio_vertical.pack()

        # Configuración de la ventana Tkinter
        self.ventana=tk.Tk()
        self.ventana.title('Inventario: Cosméticos y Otros')
        w, h = 1470, 760
        x_pos = self.ventana.winfo_screenwidth() // 2 - w // 2
        y_pos = 0
        self.ventana.geometry(f"{w}x{h}+{x_pos}+{y_pos}")
        self.ventana.resizable(0,0)
        self.ventana.config(bd=10, bg="#faf0ef")
        
        # Configuración de la barra de menú
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu = menubar)
        
        # Configuración del menú de archivo
        filemenu = tk.Menu(menubar, tearoff=0)
        inventarios = tk.Menu(filemenu, tearoff=0)
        
        menubar.add_cascade(label="Opciones",menu=filemenu)
        filemenu.add_cascade(label="Inventarios",menu=inventarios)
        inventarios.add_command(label="Cosméticos y Otros",command=self.abrir_inventario1)
        inventarios.add_command(label="Perfumes",command=self.abrir_inventario2)
        filemenu.add_separator()
        filemenu.add_command(label="Atrás",command=self.atras)
        filemenu.add_command(label="Salir",command=self.salir)
        
        # Etiqueta de título
        titulo = tk.Label(self.ventana, bg="#faf0ef", text="SENSORIAL STORE: INVENTARIO DE COSMÉTICOS Y OTROS", fg="black", font=('Comic Sans MS',27,"bold"), pady=10).pack()
        
        # Configuración de imágenes de logo y productos
        frame_logo_productos = tk.LabelFrame(self.ventana)
        frame_logo_productos.config(bd=0, bg="#faf0ef")
        frame_logo_productos.pack()
        
        imagen_makeup = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/makeup.png").resize((90,90)))
        label_imagen = tk.Label(frame_logo_productos, image=imagen_makeup, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=0, padx=15, pady=5)
        
        imagen_perfume = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/perfume.jpg").resize((90,90)))
        label_imagen = tk.Label(frame_logo_productos, image=imagen_perfume, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=1, padx=15, pady=5)
        
        imagen_logo = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/sensorial.png").resize((95,90)))
        label_imagen = tk.Label(frame_logo_productos, image=imagen_logo, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=2, padx=15, pady=5)
        
        imagen_papeleria = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/papeleria.png").resize((90,90)))
        label_imagen = tk.Label(frame_logo_productos, image=imagen_papeleria, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=3, padx=15, pady=5)
        
        imagen_cuidado = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/cuidado.jpg").resize((90,90)))
        label_imagen = tk.Label(frame_logo_productos, image=imagen_cuidado, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=4, padx=15, pady=5)
        
        espacio_vertical(self)
        
        # Sección de entrada de información
        marco = tk.LabelFrame(self.ventana,text="Información del Producto",font=("Comic Sans MS",10,"bold"),pady=5)
        marco.config(bd=2)
        marco.pack()
        
        label_codigo = tk.Label(marco, text="Código del Producto: ", font=("Comic Sans MS",10,"bold")).grid(row=0,column=0,sticky='w',padx=5,pady=8)
        self.codigo = ttk.Entry(marco,width=25)
        self.codigo.focus()
        self.codigo.grid(row=0,column=1,padx=5,pady=8,sticky="w")
        self.codigo.bind("<Return>", lambda event=None: self.combo_categoria.focus_set())
        
        label_categoria = tk.Label(marco,text="Categoría del Producto: ",font=("Comic Sans MS",10,"bold")).grid(row=0,column=2,sticky='w',padx=5,pady=9)
        self.combo_categoria = ttk.Combobox(marco,values=["Maquillaje","Cuidado Personal","Papelería"],width=22,state="readonly")
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=0,column=3,padx=5,pady=8,sticky="w")
        self.combo_categoria.bind("<Return>", lambda event=None: self.marca.focus_set())
        
        label_marca = tk.Label(marco,text="Marca del Producto: ",font=("Comic Sans MS",10,"bold")).grid(row=1,column=0,sticky='w',padx=5,pady=8)
        self.marca = tk.Entry(marco,width=25)
        self.marca.grid(row=1,column=1,padx=5,pady=8,sticky="w")
        self.marca.bind("<Return>", lambda event=None: self.descripcion.focus_set())
        
        label_descripcion = tk.Label(marco,text="Descripción del Producto: ",font=("Comic Sans MS",10,"bold")).grid(row=1,column=2,sticky='w',padx=5,pady=8)
        self.descripcion = tk.Entry(marco,width=25)
        self.descripcion.grid(row=1,column=3,padx=5,pady=8,sticky="w")
        self.descripcion.bind("<Return>", lambda event=None: self.precio_compra.focus_set())
        
        label_precio_compra = tk.Label(marco,text="Precio de Compra: ",font=("Comic Sans MS",10,"bold")).grid(row=2,column=0,sticky='w',padx=5,pady=8)
        self.precio_compra = tk.Entry(marco,width=25)
        self.precio_compra.grid(row=2,column=1,padx=5,pady=8,sticky="w")
        self.precio_compra.bind("<Return>", lambda event=None: self.precio_venta.focus_set())
        
        label_precio_venta = tk.Label(marco,text="Precio de Venta: ",font=("Comic Sans MS",10,"bold")).grid(row=2,column=2,sticky='w',padx=5,pady=8)
        self.precio_venta = tk.Entry(marco,width=25)
        self.precio_venta.grid(row=2,column=3,padx=5,pady=8,sticky="w")
        self.precio_venta.bind("<Return>", lambda event=None: self.existencias.focus_set())
        
        self.numero = tk.IntVar()
        self.numero.set(0)
        
        label_existencias = tk.Label(marco,text="Cantidad de Existencias: ",font=("Comic Sans MS",10,"bold")).grid(row=3,column=0,sticky='w',padx=5,pady=8)
        self.existencias = tk.Entry(marco,width=14,textvariable=self.numero)
        self.existencias.grid(row=3,column=1,padx=5,pady=8,sticky="w")
        self.existencias.icursor(tk.END)
        
        #Configuración botones incrementar y decrementar
        btn_incrementar = tk.Button(marco,text="↑",font=("Arial",7),bd=2,width=3,command=self.incrementar).grid(row=3,column=1,sticky='w',padx=(98,0),pady=8)
        btn_decrementar = tk.Button(marco,text="↓",font=("Arial",7),bd=2,width=3,command=self.decrementar).grid(row=3,column=1,sticky='w',padx=(128,0),pady=8)
        
        espacio_vertical(self)

        # Botones y sus acciones
        frame_botones = tk.Frame(self.ventana)
        frame_botones.config(bg="white")
        frame_botones.pack()
        
        boton_nuevo = tk.Button(frame_botones,text="LIMPIAR",height=1,width=10,bg="blue",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.nuevo).grid(row=0, column=0, padx=10, pady=10)
        boton_registrar = tk.Button(frame_botones,text="REGISTRAR",height=1,width=10,bg="green",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.create).grid(row=0, column=1, padx=10, pady=10)
        boton_editar = tk.Button(frame_botones,text="EDITAR",height=1,width=10,bg="gray",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.update).grid(row=0, column=2, padx=10, pady=10)
        boton_delete = tk.Button(frame_botones,text="BORRAR",height=1,width=10,bg="red",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.delete).grid(row=0, column=3, padx=10, pady=10)
        
        espacio_vertical(self)
        
        # Configuración de Treeview para mostrar datos
        self.tree = ttk.Treeview(height=13, columns=("columna1", "columna2", "columna3", "columna4", "columna5", "columna6"))
        self.tree.heading("#0", text='Código', anchor=tk.CENTER)
        self.tree.column("#0", width=180, minwidth=180, stretch=tk.NO)

        self.tree.heading("columna1", text='Categoría', anchor=tk.CENTER)
        self.tree.column("columna1", width=205, minwidth=205, stretch=tk.NO)

        self.tree.heading("columna2", text='Marca', anchor=tk.CENTER)
        self.tree.column("columna2", width=205, minwidth=205, stretch=tk.NO)

        self.tree.heading("columna3", text='Descripción', anchor=tk.CENTER)
        self.tree.column("columna3", width=205, minwidth=205, stretch=tk.NO)

        self.tree.heading("columna4", text='Precio de Compra', anchor=tk.CENTER)
        self.tree.column("columna4", width=205, minwidth=205, stretch=tk.NO)

        self.tree.heading("columna5", text='Precio de Venta', anchor=tk.CENTER)
        self.tree.column("columna5", width=205, minwidth=205, stretch=tk.NO)
        
        self.tree.heading("columna6", text='Existencias', anchor=tk.CENTER)
        self.tree.column("columna6", width=205, minwidth=205, stretch=tk.NO)
        
        # Configuración de la barra de desplazamiento para Treeview
        scrollbar_vertical = ttk.Scrollbar(self.ventana, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_vertical.set)
        # Ubicación de Treeview y barra de desplazamiento
        self.tree.pack(side="left", fill="both", padx=(10, 0), pady=10)
        scrollbar_vertical.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Configuración para el redimensionamiento de la cuadrícula
        self.ventana.grid_rowconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)
           
        # Vinculación de eventos     
        self.tree.bind("<ButtonRelease-1>", self.cargar_datos_seleccionados)
        self.ventana.bind("<Button-1>", self.deseleccionar_registro)

        self.read()

        self.ventana.mainloop()
        
class Inventario2:
    
    db_name='sensorial.db'
    
    # Función para validar si un valor es un número
    def validar_es_numero(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    # Función para deseleccionar un registro en el árbol al hacer clic fuera de él
    def deseleccionar_registro(self, event=None):
        if event and event.widget == self.ventana:
            self.tree.selection_remove(self.tree.selection())
            self.nuevo()
    
    # Función para cargar los datos de un registro seleccionado en el formulario
    def cargar_datos_seleccionados(self,event):
        
        self.tree.focus_set()
        if self.tree.selection():
            item = self.tree.selection()[0]
            valores = self.tree.item(item, 'values')
            codigo = self.tree.item(item, 'text')
            print(valores)

            self.codigo.delete(0, tk.END)
            self.categoria.set("")
            self.marca.delete(0, tk.END)
            self.descripcion.delete(0, tk.END)
            self.cantidad.delete(0, tk.END)
            
            self.codigo.insert(0, codigo)
            if len(valores) > 0:
                self.categoria.set(valores[0])
            if len(valores) > 1:
                self.marca.insert(0, valores[1])
            if len(valores) > 2:
                self.descripcion.insert(0, valores[2])
            if len(valores) > 3:
                self.cantidad.insert(0, valores[3])
    
    # Función para validar si hay un registro seleccionado en el árbol      
    def validar_registro_seleccionado(self):
        selected_item = self.tree.selection()
            
        if not selected_item:
            messagebox.showerror("ERROR", "Por favor, selecciona un registro.")
            return False
        else:
            return True
    
     # Función para validar si todos los campos del formulario están completos
    def validar_formulario_completo(self):
        if len(self.categoria.get()) !=0 and len(self.marca.get()) !=0 and len(self.descripcion.get()) !=0 and len(self.cantidad.get()) !=0:
            return True
        else:
             messagebox.showerror("ERROR", "Por favor, completa todos los campos del formulario.")
    
    # Función para ejecutar consultas en la base de datos
    def ejecutar_consulta(self, query, parameters=()):
        try:
            with sqlite3.connect(self.db_name) as conexion:
                cursor=conexion.cursor()
                result=cursor.execute(query,parameters)
                conexion.commit()
                print("Conexión exitosa.")
            return result
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
    
    # Función para eliminar un registro    
    def delete(self):
        if self.validar_registro_seleccionado():
                selected_item = self.tree.selection()
                descripcion = self.descripcion.get()
                codigo_producto = int(self.tree.item(selected_item)['text'])
                respuesta = messagebox.askyesno("ADVERTENCIA", f"¿Seguro que deseas eliminar el producto: {self.descripcion.get()}?")
                if respuesta:
                    query = "UPDATE inventario2 SET activo=?, eliminado=? WHERE codigo=?"
                    parameters = (0, 1, codigo_producto)
                    self.ejecutar_consulta(query, parameters)

                    messagebox.showinfo("ELIMINACIÓN EXITOSA", f'Producto eliminado: {descripcion}')
                    print(f"ELIMINADO")
                    self.read()
                    self.nuevo()
                    
    # Función para actualizar un registro     
    def update(self):
        if self.validar_registro_seleccionado():
            if self.validar_formulario_completo():
                if self.validar_es_numero(self.cantidad.get()):
                    codigo_producto = int(self.codigo.get())
                    query = 'UPDATE inventario2 SET categoria=?, marca=?, descripcion=?, cantidad=? WHERE codigo=?'
                    parameters = (
                        self.categoria.get(),
                        self.marca.get(),
                        self.descripcion.get(),
                        int(self.cantidad.get()),
                        codigo_producto
                    )
                    self.ejecutar_consulta(query, parameters)
                    messagebox.showinfo("ACTUALIZACIÓN EXITOSA.", f'Producto actualizado: {self.descripcion.get()}')
                    print('ACTUALIZADO')
                    self.read()
                    self.nuevo()
                    
                else:
                    messagebox.showerror("ERROR", "Por favor, ingresa valores numéricos en los campos correspondientes.")
    
    # Función para leer los registros de la base de datos y mostrarlos en el árbol
    def read(self):
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        query='SELECT codigo, categoria, marca, descripcion, cantidad FROM inventario2 WHERE activo=1 AND eliminado=0 ORDER BY codigo DESC'
        db_rows=self.ejecutar_consulta(query)
        
        for row in db_rows:
            self.tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
    
    # Función para crear un nuevo registro
    def create(self):
        if self.validar_formulario_completo():
            if self.validar_es_numero(self.cantidad.get()):

                query_last_inactive_code = 'SELECT MAX(codigo) FROM inventario2 WHERE activo=0 AND eliminado=1'
                result = self.ejecutar_consulta(query_last_inactive_code)
                last_inactive_code = result.fetchone()[0]

                if last_inactive_code is not None:
                    new_code = last_inactive_code
                    query_update_code = 'UPDATE inventario2 SET activo=?, eliminado=? WHERE codigo=?'
                    parameters_update_code = (1, 0, last_inactive_code)
                    self.ejecutar_consulta(query_update_code, parameters_update_code)
                    
                else:
                    query_last_code = 'SELECT MAX(codigo) FROM inventario2'
                    result = self.ejecutar_consulta(query_last_code)
                    last_code = result.fetchone()[0] or 0
                    new_code = last_code + 1

                query = 'INSERT INTO inventario2 (codigo, categoria, marca, descripcion, cantidad, activo, eliminado) VALUES(?,?,?,?,?,?,?)'
                parameters = (new_code, self.categoria.get(), self.marca.get(), self.descripcion.get(), int(self.cantidad.get()), 1, 0)
                self.ejecutar_consulta(query, parameters)

                messagebox.showinfo("REGISTRO EXITOSO.", f'Producto registrado: {self.descripcion.get()}')
                print('REGISTRADO')
                self.read()
                self.nuevo()
                
            else:
                messagebox.showerror("ERROR", "Por favor, ingresa valores numéricos en los campos correspondientes.")
    
    # Función para limpiar el formulario y prepararlo para un nuevo registro
    def nuevo(self):
        self.codigo.delete(0, tk.END)
        self.categoria.set("")
        self.categoria.set(self.categoria["values"][0])
        self.marca.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.cantidad.insert(0, "0")
        self.codigo.focus_set()
        self.deseleccionar_registro()
    
    # Funciones para incrementar y decrementar la cantidad de existencias
    def decrementar(self):
        valor_actual = tk.IntVar()
        
        valor_actual = (self.numero.get())
        
        if valor_actual > 0:
            nuevo_valor = valor_actual - 1
            self.numero.set(int(nuevo_valor))
            self.cantidad.icursor(len(str(nuevo_valor)))
    
    def incrementar(self):
        
        valor_actual = (self.numero.get())
        
        if valor_actual < 50:
        
            nuevo_valor = valor_actual + 1
            self.numero.set(int(nuevo_valor))
            self.cantidad.icursor(len(str(nuevo_valor)))
    
    # Funciones para redirigir a otras secciones del inventario, ir al menú principal y salir del módulo
    def abrir_inventario1(self):
        
        self.ventana.destroy()
        Inventario1()
    
    def abrir_inventario2(self):
        
        self.ventana.destroy()
        Inventario2()
        
    def atras(self):
        
        self.ventana.destroy()
        Menu()
        
    def salir(self):
            
        conn = sqlite3.connect('sensorial.db')

        cursor = conn.cursor()
        
        respuesta = messagebox.askyesno("ADVERTENCIA","¿Seguro que deseas cerrar la sesión?")
        if respuesta:
        
            query = "UPDATE users SET activo=0 WHERE id=1;"
            cursor.execute(query)
            
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(message="CIERRE DE SESIÓN EXISTOSO",title="Mensaje")
            print("SESIÓN CERRADA")
            self.ventana.destroy()
            App()
            self.ventana.destroy()
            Ventas()

    def __init__(self):
        
        # Función para crear un espacio vertical en la interfaz
        def espacio_vertical(self):
            espacio_vertical = tk.Frame(self.ventana, height=20, bg="#faf0ef")
            espacio_vertical.pack()
    
        # Inicialización de la ventana principal
        self.ventana=tk.Tk()
        self.ventana.title('Inventario: Perfumes')
        w, h = 1470, 760
        x_pos = self.ventana.winfo_screenwidth() // 2 - w // 2
        y_pos = 0
        self.ventana.geometry(f"{w}x{h}+{x_pos}+{y_pos}")
        self.ventana.resizable(0,0)
        self.ventana.config(bd=10, bg="#faf0ef")
        
        # Configuración del menú
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu = menubar)
        filemenu = tk.Menu(menubar, tearoff=0)
        inventarios = tk.Menu(filemenu, tearoff=0)
        menubar.add_cascade(label="Opciones",menu=filemenu)
        filemenu.add_cascade(label="Inventarios",menu=inventarios)
        inventarios.add_command(label="Cosméticos y Otros",command=self.abrir_inventario1)
        inventarios.add_command(label="Perfumes",command=self.abrir_inventario2)
        filemenu.add_separator()
        filemenu.add_command(label="Atrás",command=self.atras)
        filemenu.add_command(label="Salir",command=self.salir)
        
        # Configuración del título
        titulo = tk.Label(self.ventana, bg="#faf0ef", text="SENSORIAL STORE: INVENTARIO DE PERFUMES", fg="black", font=('Comic Sans MS',30,"bold"), pady=10).pack()
        
        # Configuración del marco de imágenes
        frame_logo_productos = tk.LabelFrame(self.ventana)
        frame_logo_productos.config(bd=0, bg="#faf0ef")
        frame_logo_productos.pack()
        
        # Configuración de las imágenes
        imagen_logo = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/sensorial.png").resize((95,90)))
        label_imagen = tk.Label(frame_logo_productos, image=imagen_logo, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=0, padx=15, pady=5)
        
        imagen_perfume = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/perfume.jpg").resize((90,90)))
        label_imagen = tk.Label(frame_logo_productos, image=imagen_perfume, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=1, padx=15, pady=5)
        
        espacio_vertical(self)
        
        # Configuración del marco de información del producto
        marco = tk.LabelFrame(self.ventana,text="Información del Producto",font=("Comic Sans MS",10,"bold"),pady=5)
        marco.config(bd=2)
        marco.pack()
        
        # Configuración de etiquetas y entradas de datos
        label_codigo = tk.Label(marco, text="Código del Producto: ", font=("Comic Sans MS",10,"bold")).grid(row=0,column=0,sticky='w',padx=5,pady=8)
        self.codigo = ttk.Entry(marco,width=25)
        self.codigo.focus()
        self.codigo.grid(row=0,column=1,padx=5,pady=8,sticky="w")
        self.codigo.bind("<Return>", lambda event=None: self.categoria.focus_set())
        
        label_categoria = tk.Label(marco, text="Categoría del Producto: ", font=("Comic Sans MS",10,"bold")).grid(row=0,column=2,sticky='w',padx=5,pady=8)
        self.categoria = ttk.Combobox(marco,values=["Perfumería"],width=22,state="readonly")
        self.categoria.current(0)
        self.categoria.grid(row=0,column=3,padx=5,pady=8,sticky="w")
        self.categoria.bind("<Return>", lambda event=None: self.marca.focus_set())
        
        label_marca = tk.Label(marco,text="Marca del Producto: ",font=("Comic Sans MS",10,"bold")).grid(row=1,column=0,sticky='w',padx=5,pady=8)
        self.marca = tk.Entry(marco,width=25)
        self.marca.grid(row=1,column=1,padx=5,pady=8,sticky="w")
        self.marca.bind("<Return>", lambda event=None: self.descripcion.focus_set())
        
        label_descripcion = tk.Label(marco,text="Descripción del Producto: ",font=("Comic Sans MS",10,"bold")).grid(row=1,column=2,sticky='w',padx=5,pady=8)
        self.descripcion = tk.Entry(marco,width=25)
        self.descripcion.grid(row=1,column=3,padx=5,pady=8,sticky="w")
        self.descripcion.bind("<Return>", lambda event=None: self.cantidad.focus_set())
        
        self.numero = tk.IntVar()
        self.numero.set(0)
        
        label_cantidad = tk.Label(marco,text="Cantidad/Gramos: ",font=("Comic Sans MS",10,"bold")).grid(row=2,column=0,sticky='w',padx=5,pady=8)
        self.cantidad = tk.Entry(marco,width=14,textvariable=self.numero)
        self.cantidad.grid(row=2,column=1,padx=5,pady=8,sticky="w")
        self.cantidad.icursor(tk.END)
        
        # Configuración de botones decrementar e incrementar
        btn_incrementar = tk.Button(marco,text="↑",font=("Arial",7),bd=2,width=3,command=self.incrementar).grid(row=2,column=1,sticky='w',padx=(98,0),pady=8)
        btn_decrementar = tk.Button(marco,text="↓",font=("Arial",7),bd=2,width=3,command=self.decrementar).grid(row=2,column=1,sticky='w',padx=(128,0),pady=8)
        
        espacio_vertical(self)

        # Configuración de botones crud
        frame_botones = tk.Frame(self.ventana)
        frame_botones.config(bg="white")
        frame_botones.pack()
        
        boton_nuevo = tk.Button(frame_botones,text="LIMPIAR",height=1,width=10,bg="blue",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.nuevo).grid(row=0, column=0, padx=10, pady=10)
        boton_registrar = tk.Button(frame_botones,text="REGISTRAR",height=1,width=10,bg="green",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.create).grid(row=0, column=1, padx=10, pady=10)
        boton_editar = tk.Button(frame_botones,text="EDITAR",height=1,width=10,bg="gray",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.update).grid(row=0, column=2, padx=10, pady=10)
        boton_editar = tk.Button(frame_botones,text="BORRAR",height=1,width=10,bg="red",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.delete).grid(row=0, column=3, padx=10, pady=10)
        
        espacio_vertical(self)
        
        # Configuración de la tabla de datos
        self.tree = ttk.Treeview(self.ventana,height=13,columns=("columna1","columna2","columna3","columna4"))
        self.tree.heading("#0",text='Código',anchor=tk.CENTER)
        self.tree.column("#0",width=180,minwidth=180,stretch=tk.NO)
        
        self.tree.heading("columna1",text='Categoría',anchor=tk.CENTER)
        self.tree.column("columna1",width=205,minwidth=205,stretch=tk.NO)
        
        self.tree.heading("columna2",text='Marca',anchor=tk.CENTER)
        self.tree.column("columna2",width=205,minwidth=205,stretch=tk.NO)
        
        self.tree.heading("columna3",text='Descripción',anchor=tk.CENTER)
        self.tree.column("columna3",width=205,minwidth=205,stretch=tk.NO)
        
        self.tree.heading("columna4",text='Cantidad/Gramos',anchor=tk.CENTER)
        self.tree.column("columna4",width=205,minwidth=205,stretch=tk.NO)
        
        # Configuración del scrollbar de la tabla de datos
        scrollbar_vertical = ttk.Scrollbar(self.ventana, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_vertical.set)
        
        self.tree.pack(side="left", fill="both", padx=(215, 0), pady=10)
        scrollbar_vertical.pack(side="right", fill="y", padx=(0, 215), pady=10)

        self.ventana.grid_rowconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        self.tree.bind("<ButtonRelease-1>", self.cargar_datos_seleccionados)
        self.ventana.bind("<Button-1>", self.deseleccionar_registro)
        
        self.read()
        
        self.ventana.mainloop()
        
class Ventas:
    
    db_name = 'sensorial.db'
    
    # Método para enfocar el campo de entrada de otros gastos al presionar una tecla 
    def mover_a_otros_gastos(self, event):
        self.otros_gastos.focus_set()
        
    # Método para calcular el porcentaje del inventario al ingresar el total de la venta
    def calcular_porcentaje_inventario(self, event):
        try:
            total_venta = float(self.total_venta.get())
            porcentaje_inventario = total_venta * 0.6
            self.inventario.delete(0, tk.END)
            self.inventario.insert(0, str(porcentaje_inventario))
            self.inventario.focus_set()
        except ValueError:
            self.validar_es_numero(self.total_venta.get())
    
    # Método para calcular el porcentaje de ganancia al ingresar el total de la venta    
    def calcular_porcentaje_ganancia(self, event):
        try:
            total_venta = float(self.total_venta.get())
            porcentaje_ganancia = total_venta * 0.4
            self.ganancia.delete(0, tk.END)
            self.ganancia.insert(0, str(porcentaje_ganancia))
            self.ganancia.focus_set()
            self.calcular_porcentaje_inventario()
            
        except ValueError:
            self.validar_es_numero(self.total_venta.get())
            
    # Métodos para calcular el total de venta al presionar Enter en diferentes campos   
    def calcular_total_venta_efectivo(self, event):
        self.calcular_total_venta()
        self.total_qr.focus_set()

    def calcular_total_venta_qr(self, event):
        self.calcular_total_venta()
        self.total_datafono.focus_set()

    def calcular_total_venta_datafono(self, event):
        self.calcular_total_venta()
        self.total_venta.focus_set()
    
    def calcular_total_venta(self):
        try:
            total_efectivo = float(self.total_efectivo.get())
            total_qr = float(self.total_qr.get())
            total_datafono = float(self.total_datafono.get())
            total_venta = total_efectivo + total_qr + total_datafono
            self.total_venta.delete(0, tk.END)
            self.total_venta.insert(0, str(total_venta))

        except ValueError:
            self.validar_es_numero(self.total_efectivo.get()) and self.validar_es_numero(self.total_qr.get()) and self.validar_es_numero(self.total_datafono.get()) and self.validar_es_numero(self.total_venta.get()) and self.validar_es_numero(self.ganancia.get()) and self.validar_es_numero(self.inventario.get()) and self.validar_es_numero(self.otros_gastos.get())
    
    # Método para validar si un valor es un número
    def validar_es_numero(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    # Método para deseleccionar un registro al hacer clic fuera del Treeview
    def deseleccionar_registro(self, event=None):
        if event and event.widget == self.ventana:
            self.tree.selection_remove(self.tree.selection())
            self.nuevo()
    
    # Método para cargar los datos del registro seleccionado en los campos de entrada
    def cargar_datos_seleccionados(self,event):
        
        self.tree.focus_set()
        if self.tree.selection():
            item = self.tree.selection()[0]
            valores = self.tree.item(item, 'values')
            codigo = self.tree.item(item, 'text')
            print(valores)

            self.codigo_venta.delete(0, tk.END)
            self.nombre_punto.delete(0, tk.END)
            self.fecha_venta.delete(0, tk.END)
            self.total_efectivo.delete(0, tk.END)
            self.total_qr.delete(0, tk.END)
            self.total_datafono.delete(0, tk.END)
            self.total_venta.delete(0, tk.END)
            self.ganancia.delete(0, tk.END)
            self.inventario.delete(0, tk.END)
            self.otros_gastos.delete(0, tk.END)
            
            self.codigo_venta.insert(0, codigo)
            if len(valores) > 0:
                self.nombre_punto.insert(0, valores[0])
            if len(valores) > 1:
                 fecha_seleccionada = datetime.strptime(valores[1], "%d-%m-%Y")
                 self.fecha_venta.set_date(fecha_seleccionada)
            if len(valores) > 2:
                self.total_efectivo.insert(0, valores[2])
            if len(valores) > 3:
                self.total_qr.insert(0, valores[3])
            if len(valores) > 4:
                self.total_datafono.insert(0, valores[4])
            if len(valores) > 5:
                self.total_venta.insert(0, valores[5])
            if len(valores) > 6:
                self.ganancia.insert(0, valores[6])
            if len(valores) > 7:
                self.inventario.insert(0, valores[7])
            if len(valores) > 8:
                self.otros_gastos.insert(0, valores[8])
    
    # Método para validar si se ha seleccionado un registro en el Treeview
    def validar_registro_seleccionado(self):
        selected_item = self.tree.selection()
            
        if not selected_item:
            messagebox.showerror("ERROR", "Por favor, selecciona un registro.")
            return False
        else:
            return True
    
    # Método para validar si todos los campos del formulario están completos
    def validar_formulario_completo(self):
        if len(self.nombre_punto.get()) !=0 and len(self.total_efectivo.get()) !=0 and len(self.total_qr.get()) !=0 and len(self.total_datafono.get()) !=0 and len(self.total_venta.get()) !=0 and len(self.ganancia.get()) !=0 and len(self.inventario.get()) !=0 and len(self.otros_gastos.get()) !=0:
            return True
        else:
             messagebox.showerror("ERROR", "Por favor, completa todos los campos del formulario.")
    
    # Método para ejecutar consultas en la base de datos
    def ejecutar_consulta(self, query, parameters=()):
        try:
            with sqlite3.connect(self.db_name) as conexion:
                cursor=conexion.cursor()
                result=cursor.execute(query,parameters)
                conexion.commit()
                print("Conexión exitosa.")
            return result
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
    
    # Método para eliminar un registro        
    def delete(self):
        if self.validar_registro_seleccionado():
                selected_item = self.tree.selection()
                codigo_producto = int(self.tree.item(selected_item)['text'])
                respuesta = messagebox.askyesno("ADVERTENCIA", f"¿Seguro que deseas eliminar la venta?")
                if respuesta:
                    query = "UPDATE ventas SET activo=?, eliminado=? WHERE codigo=?"
                    parameters = (0, 1, codigo_producto)
                    self.ejecutar_consulta(query, parameters)

                    messagebox.showinfo("ELIMINACIÓN EXITOSA.", f'Venta Eliminada')
                    print(f"ELIMINADO")
                    self.read()
                    self.nuevo()
    
    # Método para actualizar un registro        
    def update(self):
        if self.validar_registro_seleccionado():
            if self.validar_formulario_completo():
                if self.validar_es_numero(self.total_efectivo.get()) and self.validar_es_numero(self.total_qr.get()) and self.validar_es_numero(self.total_datafono.get()) and self.validar_es_numero(self.total_venta.get()) and self.validar_es_numero(self.ganancia.get()) and self.validar_es_numero(self.inventario.get()) and self.validar_es_numero(self.otros_gastos.get()):
                     
                    codigo_producto = int(self.codigo_venta.get())
                    query = 'UPDATE ventas SET nombre_punto=?, fecha=?, efectivo=?, qr=?, datafono=?, venta=?, ganancia=?, inventario=?, otros_gastos=? WHERE codigo=?'
                    parameters = (
                        self.nombre_punto.get(), 
                        self.fecha_venta.get(), 
                        float(self.total_efectivo.get()), 
                        float(self.total_qr.get()), 
                        float(self.total_datafono.get()), 
                        float(self.total_venta.get()), 
                        float(self.ganancia.get()), 
                        float(self.inventario.get()), 
                        float(self.otros_gastos.get()),
                        codigo_producto
                    )
                    self.ejecutar_consulta(query, parameters)
                    messagebox.showinfo("ACTUALIZACIÓN EXITOSA.",'Venta Actualizada')
                    print('ACTUALIZADO')
                    self.read()
                    self.nuevo()
                    
                else:
                    messagebox.showerror("ERROR", "Por favor, ingresa valores numéricos en los campos correspondientes.")    
    
    # Ubicar los registros existentes en el Treeview
    def read(self):
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        query='SELECT codigo, nombre_punto, fecha, efectivo, qr, datafono, venta, ganancia, inventario, otros_gastos, activo, eliminado FROM ventas WHERE activo=1 AND eliminado=0 ORDER BY codigo DESC'
        db_rows=self.ejecutar_consulta(query)
        
        for row in db_rows:
            self.tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
    
    # Crear un nuevo registro en la base de datos
    def create(self):
        if self.validar_formulario_completo():
            if self.validar_es_numero(self.total_efectivo.get()) and self.validar_es_numero(self.total_qr.get()) and self.validar_es_numero(self.total_datafono.get()) and self.validar_es_numero(self.total_venta.get()) and self.validar_es_numero(self.ganancia.get()) and self.validar_es_numero(self.inventario.get()) and self.validar_es_numero(self.otros_gastos.get()):

                query_last_inactive_code = 'SELECT MAX(codigo) FROM ventas WHERE activo=0 AND eliminado=1'
                result = self.ejecutar_consulta(query_last_inactive_code)
                last_inactive_code = result.fetchone()[0]

                if last_inactive_code is not None:
                    new_code = last_inactive_code
                    query_update_code = 'UPDATE ventas SET activo=?, eliminado=? WHERE codigo=?'
                    parameters_update_code = (1, 0, last_inactive_code)
                    self.ejecutar_consulta(query_update_code, parameters_update_code)
                    
                else:
                    query_last_code = 'SELECT MAX(codigo) FROM ventas'
                    result = self.ejecutar_consulta(query_last_code)
                    last_code = result.fetchone()[0] or 0
                    new_code = last_code + 1

                query = 'INSERT INTO ventas (codigo, nombre_punto, fecha, efectivo, qr, datafono, venta, ganancia, inventario, otros_gastos, activo, eliminado) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'
                parameters = (new_code, self.nombre_punto.get(), self.fecha_venta.get(), float(self.total_efectivo.get()), float(self.total_qr.get()), float(self.total_datafono.get()), float(self.total_venta.get()), float(self.ganancia.get()), float(self.inventario.get()), float(self.otros_gastos.get()), 1, 0)
                self.ejecutar_consulta(query, parameters)

                messagebox.showinfo("REGISTRO EXITOSO.",'Venta Registrada')
                print('REGISTRADO')
                self.read()
                self.nuevo()
                
            else:
                messagebox.showerror("ERROR", "Por favor, ingresa valores numéricos en los campos correspondientes.")
    
    # Limpiar los campos de entrada para crear un nuevo registro
    def nuevo(self):
        self.codigo_venta.delete(0, tk.END)
        self.codigo_venta.focus_set()
        
        self.nombre_punto.delete(0, tk.END)
        self.nombre_punto.insert(0, "Sensorial Store")
        
        fecha_actual = datetime.now().date()
        self.fecha_venta.delete(0, tk.END)
        self.fecha_venta.set_date(fecha_actual)
        
        self.total_efectivo.delete(0, tk.END)
        self.total_qr.delete(0, tk.END)
        self.total_datafono.delete(0, tk.END)
        self.total_venta.delete(0, tk.END)
        self.ganancia.delete(0, tk.END)
        self.inventario.delete(0, tk.END)
        
        self.otros_gastos.delete(0, tk.END)
        self.otros_gastos.insert(0, "0")
    
    # Navegar de nuevo al menú principal
    def atras(self):
        
        self.ventana.destroy()
        Menu()
    
    # Cerrar sesión y actualizar el estado del usuario
    def salir(self):
        
        respuesta = messagebox.askyesno("ADVERTENCIA","¿Seguro que deseas cerrar la sesión?")
        if respuesta:
        
            query = "UPDATE users SET activo=0 WHERE id=1;"
            self.ejecutar_consulta(query)

            messagebox.showinfo(message="CIERRE DE SESIÓN EXISTOSO",title="Mensaje")
            print("SESIÓN CERRADA")
            self.ventana.destroy()
            App()

    def __init__(self):
        
        # Función interna para crear un espacio vertical
        def espacio_vertical(self):
            espacio_vertical = tk.Frame(self.ventana, height=10, bg="#faf0ef")
            espacio_vertical.pack()
        
        # Configuración de la ventana principal
        self.ventana=tk.Tk()
        self.ventana.title('Ventas')
        w, h = 1470, 760
        x_pos = self.ventana.winfo_screenwidth() // 2 - w // 2
        y_pos = 0
        self.ventana.geometry(f"{w}x{h}+{x_pos}+{y_pos}")
        self.ventana.resizable(0,0)
        self.ventana.config(bd=10, bg="#f2f8ec")
        
        # Configuración del menú
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu = menubar)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones",menu=filemenu)
        filemenu.add_command(label="Atrás",command=self.atras)
        filemenu.add_command(label="Salir",command=self.salir)
        
        # Configuración del título y logotipos
        titulo = tk.Label(self.ventana, bg="#f2f8ec", text="SENSORIAL STORE: VENTAS", fg="black", font=('Comic Sans MS', 27, "bold"),pady=10).pack()
        
        frame_logo_ventas = tk.LabelFrame(self.ventana)
        frame_logo_ventas.config(bd=0, bg="#f2f8ec")
        frame_logo_ventas.pack()
        
        imagen_logo = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/sensorial.png").resize((100,90)))
        label_imagen = tk.Label(frame_logo_ventas, image=imagen_logo, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=0, padx=15, pady=5)
               
        imagen_venta = ImageTk.PhotoImage(Image.open(os.getcwd()+"./images/venta.jpg").resize((140,90)))
        label_imagen = tk.Label(frame_logo_ventas, image=imagen_venta, bg="#faf0ef", bd=2, relief="solid")
        label_imagen.grid(row=0, column=1, padx=15, pady=5)
        
        espacio_vertical(self)
        
        # Configuración del marco de información de venta
        marco = tk.LabelFrame(self.ventana,text="Información de la Venta",font=("Comic Sans MS",10,"bold"),pady=5)
        marco.config(bd=2)
        marco.pack()
        
        # Configuración de etiquetas y campos de entrada para la información de la venta
        label_codigo_venta = tk.Label(marco, text="Código de la Venta: ", font=("Comic Sans MS",10,"bold")).grid(row=0,column=0,sticky='w',padx=5,pady=8)
        self.codigo_venta = ttk.Entry(marco,width=25)
        self.codigo_venta.focus()
        self.codigo_venta.grid(row=0,column=1,padx=5,pady=8,sticky="w")
        self.codigo_venta.bind("<Return>", lambda event=None: self.nombre_punto.focus_set())
        
        label_nombre_punto = tk.Label(marco,text="Nombre del Punto: ",font=("Comic Sans MS",10,"bold")).grid(row=0,column=2,sticky='w',padx=5,pady=9)
        self.nombre_punto = ttk.Entry(marco,width=25)
        self.nombre_punto.insert(0, "Sensorial Store")
        self.nombre_punto.grid(row=0,column=3,padx=5,pady=8,sticky="w")
        self.nombre_punto.bind("<Return>", lambda event=None: self.fecha_venta.focus_set())
        
        label_fecha_venta = tk.Label(marco,text="Fecha de la Venta: ",font=("Comic Sans MS",10,"bold")).grid(row=1,column=0,sticky='w',padx=5,pady=8)
        self.fecha_venta = DateEntry(marco, width=22, background="green", foreground="white", borderwidth=2, date_pattern="dd-mm-yyyy")
        self.fecha_venta.grid(row=1,column=1,padx=5,pady=8,sticky="w")
        self.fecha_venta.bind("<Return>", lambda event=None: self.total_efectivo.focus_set())
        
        label_total_efectivo = tk.Label(marco,text="Total Efectivo: ",font=("Comic Sans MS",10,"bold")).grid(row=1,column=2,sticky='w',padx=5,pady=8)
        self.total_efectivo = tk.Entry(marco,width=25)
        self.total_efectivo.grid(row=1,column=3,padx=5,pady=8,sticky="w")
        
        label_total_qr = tk.Label(marco,text="Total QR: ",font=("Comic Sans MS",10,"bold")).grid(row=2,column=0,sticky='w',padx=5,pady=8)
        self.total_qr = tk.Entry(marco,width=25)
        self.total_qr.grid(row=2,column=1,padx=5,pady=8,sticky="w")
        
        label_total_datafono = tk.Label(marco,text="Total Datáfono: ",font=("Comic Sans MS",10,"bold")).grid(row=2,column=2,sticky='w',padx=5,pady=8)
        self.total_datafono = tk.Entry(marco,width=25)
        self.total_datafono.grid(row=2,column=3,padx=5,pady=8,sticky="w")
        
        label_total_venta = tk.Label(marco,text="Total Venta: ",font=("Comic Sans MS",10,"bold")).grid(row=3,column=0,sticky='w',padx=5,pady=8)
        self.total_venta = tk.Entry(marco,width=25)
        self.total_venta.grid(row=3,column=1,padx=5,pady=8,sticky="w")
        
        label_ganancia = tk.Label(marco,text="Ganancia: ",font=("Comic Sans MS",10,"bold")).grid(row=3,column=2,sticky='w',padx=5,pady=8)
        self.ganancia = tk.Entry(marco,width=25)
        self.ganancia.grid(row=3,column=3,padx=5,pady=8,sticky="w")
        
        label_inventario = tk.Label(marco,text="Inventario: ",font=("Comic Sans MS",10,"bold")).grid(row=4,column=0,sticky='w',padx=5,pady=8)
        self.inventario = tk.Entry(marco,width=25)
        self.inventario.grid(row=4,column=1,padx=5,pady=8,sticky="w")
        
        label_otros_gastos = tk.Label(marco,text="Otros Gastos: ",font=("Comic Sans MS",10,"bold")).grid(row=4,column=2,sticky='w',padx=5,pady=8)
        self.otros_gastos = tk.Entry(marco,width=25)
        self.otros_gastos.grid(row=4,column=3,padx=5,pady=8,sticky="w")
        self.otros_gastos.insert(0, "0")
        
        self.total_efectivo.bind("<Return>", self.calcular_total_venta_efectivo)
        self.total_qr.bind("<Return>", self.calcular_total_venta_qr)
        self.total_datafono.bind("<Return>", self.calcular_total_venta_datafono)
        self.total_venta.bind("<Return>", self.calcular_porcentaje_ganancia)
        self.ganancia.bind("<Return>", self.calcular_porcentaje_inventario)
        self.inventario.bind("<Return>", self.mover_a_otros_gastos)
        
        espacio_vertical(self)
        
        # Configuración botones y sus acciones
        
        frame_botones = tk.Frame(self.ventana)
        frame_botones.config(bg="white")
        frame_botones.pack()
        
        boton_nuevo = tk.Button(frame_botones,text="LIMPIAR",height=1,width=10,bg="blue",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.nuevo).grid(row=0, column=0, padx=10, pady=10)
        boton_registrar = tk.Button(frame_botones,text="REGISTRAR",height=1,width=10,bg="green",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.create).grid(row=0, column=1, padx=10, pady=10)
        boton_editar = tk.Button(frame_botones,text="EDITAR",height=1,width=10,bg="gray",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.update).grid(row=0, column=2, padx=10, pady=10)
        boton_delete = tk.Button(frame_botones,text="BORRAR",height=1,width=10,bg="red",fg="white",font=("Comic Sans MS", 10,"bold"),command=self.delete).grid(row=0, column=3, padx=10, pady=10)
        
        espacio_vertical(self)
        
        # Configuración de la tabla de datos visual    
        self.tree = ttk.Treeview(height=13, columns=("columna1", "columna2", "columna3", "columna4", "columna5", "columna6", "columna7", "columna8", "columna9"))
        self.tree.heading("#0", text='Código', anchor=tk.CENTER)
        self.tree.column("#0", width=140, minwidth=140, stretch=tk.NO)

        self.tree.heading("columna1", text='Punto', anchor=tk.CENTER)
        self.tree.column("columna1", width=140, minwidth=140, stretch=tk.NO)
        
        self.tree.heading("columna2", text='Fecha', anchor=tk.CENTER)
        self.tree.column("columna2", width=140, minwidth=140, stretch=tk.NO)

        self.tree.heading("columna3", text='Total Efectivo', anchor=tk.CENTER)
        self.tree.column("columna3", width=140, minwidth=140, stretch=tk.NO)
        
        self.tree.heading("columna4", text='Total QR', anchor=tk.CENTER)
        self.tree.column("columna4", width=140, minwidth=140, stretch=tk.NO)

        self.tree.heading("columna5", text='Total Data', anchor=tk.CENTER)
        self.tree.column("columna5", width=140, minwidth=140, stretch=tk.NO)

        self.tree.heading("columna6", text='Total Venta', anchor=tk.CENTER)
        self.tree.column("columna6", width=140, minwidth=140, stretch=tk.NO)
        
        self.tree.heading("columna7", text='Ganancia', anchor=tk.CENTER)
        self.tree.column("columna7", width=140, minwidth=140, stretch=tk.NO)
        
        self.tree.heading("columna8", text='Inventario', anchor=tk.CENTER)
        self.tree.column("columna8", width=140, minwidth=140, stretch=tk.NO)
        
        self.tree.heading("columna9", text='Otros Gastos', anchor=tk.CENTER)
        self.tree.column("columna9", width=140, minwidth=140, stretch=tk.NO)
        
        scrollbar_vertical = ttk.Scrollbar(self.ventana, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_vertical.set)
        
        self.tree.pack(side="left", fill="both", padx=(15, 0), pady=10)
        scrollbar_vertical.pack(side="right", fill="y", padx=(0, 15), pady=10)

        self.ventana.grid_rowconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)
        
        # Configuración de eventos de clic para el Treeview y la ventana
        self.tree.bind("<ButtonRelease-1>", self.cargar_datos_seleccionados)
        self.ventana.bind("<Button-1>", self.deseleccionar_registro)
        
        self.read()
            
        self.ventana.mainloop()
    