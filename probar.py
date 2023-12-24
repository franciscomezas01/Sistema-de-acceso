import tkinter as tk
from tkinter import ttk
import sqlite3
import serial
import datetime
from dateutil.relativedelta import relativedelta
import time
import pandas as pd
from tkinter import END 


class Acceso:
    
    db_name = 'acceso.db'
    
    def __init__(self, root):
        self.root = root
        self.root.title("Cambiar Funciones en la Misma Ventana")

        # Crear los marcos
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(pady=50, padx=50)

        self.frame_agregar = ttk.LabelFrame(self.frame_principal, text="Usuario")
        self.frame_agregar.grid(row=0, column=0, pady=20, padx=10)

        self.frame_agregar_usuarios = ttk.Frame(self.root)  # Inicializar aquí
        self.frame_agregar_usuarios.pack_forget()  # Ocultar por defecto
        
        self.frame_formulario_edicion = ttk.Frame(self.root)  # Inicializar aquí
        self.frame_formulario_edicion.pack_forget()  # Ocultar por defecto

        ttk.Button(self.frame_agregar, text='Agregar', command=self.mostrar_agregar, style='TButton').grid(
            row=0, column=0, padx=10, sticky=tk.W + tk.E, columnspan=2)
        ttk.Button(self.frame_agregar, text='Eliminar', command=self.mostrar_formulario_eliminar, style='TButton').grid(
            row=1, column=0, padx=10, sticky=tk.W + tk.E, columnspan=2)
        ttk.Button(self.frame_agregar, text='Actualizar datos', command=self.formulario_edit, style='TButton').grid(
            row=2, column=0, padx=10, sticky=tk.W + tk.E, columnspan=2)

        self.frame_leer = ttk.LabelFrame(self.frame_principal, text="Ingreso")
        self.frame_leer.grid(row=0, column=1, pady=20, padx=10)

        ttk.Button(self.frame_leer, text='Tarjeta', command=self.entrar_tarjeta, style='TButton').grid(
            row=0, column=0, sticky=tk.W + tk.E)
        ttk.Button(self.frame_leer, text='Documento', command=self.mostrar_formulario_dni_ingreso_documento, style='TButton').grid(
            row=1, column=0, sticky=tk.W + tk.E)

        self.frame_sumar_mes = ttk.LabelFrame(self.frame_principal, text="Sumar")
        self.frame_sumar_mes.grid(row=1, column=1, pady=20, padx=10)

        ttk.Button(self.frame_sumar_mes, text='Sumar mes', command=self.mostrar_formulario_dni_sumar_mes, style='TButton').grid(
            row=0, column=0, sticky=tk.W + tk.E)
        ttk.Button(self.frame_sumar_mes, text='Sumar 6 meses', command=self.mostrar_formulario_dni_sumar_mes, style='TButton').grid(
            row=1, column=0, sticky=tk.W + tk.E)
        ttk.Button(self.frame_sumar_mes, text='Sumar un año', command= self.mostrar_formulario_dni_sumar_mes, style='TButton').grid(
            row=2, column=0, sticky=tk.W + tk.E)

        self.frame_excel = ttk.LabelFrame(self.frame_principal, text="Exportar")
        self.frame_excel.grid(row=1, column=0, pady=20, padx=10)
        ttk.Button(self.frame_excel, text='excel', command=self.exportar_a_excel, style='TButton').grid(
            row=0, column=0, sticky=tk.W + tk.E)

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parameters)
            conn.commit()
        return resultado

    def mostrar_agregar(self):
        # Ocultar el marco principal
        self.frame_principal.pack_forget()

        # Mostrar el marco de agregar usuarios
        self.frame_agregar_usuarios.pack(pady=50, padx=50)

        tk.Label(self.frame_agregar_usuarios, text="Nombre: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.nombre = tk.Entry(self.frame_agregar_usuarios)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        tk.Label(self.frame_agregar_usuarios, text="Apellido: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=2, column=0)
        self.apellido = tk.Entry(self.frame_agregar_usuarios)
        self.apellido.grid(row=2, column=1)

        tk.Label(self.frame_agregar_usuarios, text="Documento: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=3, column=0)
        self.documento = tk.Entry(self.frame_agregar_usuarios)
        self.documento.grid(row=3, column=1)

        tk.Label(self.frame_agregar_usuarios, text="Plan(2-6): ", font=('Helvetica', 12), bg='#FFA07A').grid(row=4, column=0)
        self.Plan = tk.Entry(self.frame_agregar_usuarios)
        self.Plan.grid(row=4, column=1)

        ttk.Button(self.frame_agregar_usuarios, text="Leer tarjeta", command=self.Leer_tarjeta, style='TButton').grid(
            row=5, columnspan=2, sticky=tk.W + tk.E)
        ttk.Button(self.frame_agregar_usuarios, text="Guardar usuario", command=self.guardar_usuario,
                   style='TButton').grid(row=6, columnspan=2, sticky=tk.W + tk.E)

        self.message = tk.Label(self.frame_agregar_usuarios, text='', fg='red', font=('Helvetica', 12, 'italic'), bg='#FFA07A')
        self.message.grid(row=7, column=0, columnspan=3, sticky=tk.W + tk.E)

    def validacion(self):
        return len(self.nombre.get()) != 0 and len(self.apellido.get()) != 0 and len(self.documento.get()) != 0

    def validar_plan(self, plan):
        try:
            plan_entero=int(plan)
            
            if 2<= plan_entero <=6:
                return True
            else:
                return False
        except ValueError:
            return False

    def guardar_usuario(self):
        try:
            dni = self.documento.get()
            plan = self.Plan.get()
            
            if not self.validar_plan(plan):
                self.message['text'] = 'Ingrese un plan válido (2-6)'
                return

        # Verifica si el DNI ya existe en la base de datos
            query_verificacion = 'SELECT * FROM clientes WHERE Dni = ?'
            parametros_verificacion = (dni,)
            resultado_verificacion = self.run_query(
                query_verificacion, parametros_verificacion)

            if resultado_verificacion.fetchone():
                # El DNI ya existe, muestra un mensaje de error
                self.message['text'] = 'El DNI {} ya existe en la base de datos'.format(
                    dni)
                self.documento.delete(0, END)
                
                #Se verifica que no exista esa tarjeta
            else:
                query_verificacion = 'SELECT * FROM clientes WHERE Tarjeta = ?'
                parametros_verificacion = (self.tarjeta_id,)
                resultado_tarjeta = self.run_query(
                query_verificacion, parametros_verificacion)
                if resultado_tarjeta.fetchone():
                    self.message['text'] = 'La tarjeta  ya existe en la base de datos'
                    self.documento.delete(0, END)
                elif self.validacion():
                    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
                #En caso de no tener arduino se puede descomentar esta linea y sacarle el self a la tarjeta para verificar almacenamiento
                #tarjeta_id = "8675309125" 
                    query = 'INSERT INTO clientes (Nombre, Apellido, Dni, Tarjeta, Fecha, Plan ) VALUES (?, ?, ?, ?, ?, ?)'
                    parametros = (self.nombre.get(), self.apellido.get(
                    ), dni, self.tarjeta_id, fecha_actual, plan)
                    self.run_query(query, parametros)

                    print("Usuario guardado en la base de datos.")
                    self.message['text'] = 'El cliente {} fue agregado'.format(
                    self.nombre.get())
                    self.nombre.delete(0, END)
                    self.apellido.delete(0, END)
                    self.documento.delete(0, END)

                    self.limpiar_interfaz()
                    print("aca no llega por que aca se ejecuta")
                else:
                    print("campos vacíos")
                    self.message['text'] = 'Un campo está vacío'

        except Exception as e:
            print("Error:", e)

    def Leer_tarjeta(self):
        arduino_port = 'COM3'
        ser = serial.Serial(arduino_port, 9600, timeout=1)
        try:
            while True:
        # Lee la línea recibida desde Arduino
                tarjeta_id = ser.readline().decode('utf-8').rstrip()
        
                if tarjeta_id:
                    print("id de tarjeta", tarjeta_id)
                    self.tarjeta_id = tarjeta_id
                    break

        except Exception as e:
            print("Error:", e)

    def formulario_edit(self):
        # Ocultar el marco principal
        self.frame_principal.pack_forget()

        # Mostrar el formulario para ingresar el DNI
        self.frame_formulario_dni = ttk.Frame(self.root)
        self.frame_formulario_dni.pack(pady=50, padx=50)

        tk.Label(self.frame_formulario_dni, text="Ingrese DNI: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=0, column=0)
        self.documento_editar = tk.Entry(self.frame_formulario_dni)
        self.documento_editar.focus()
        self.documento_editar.grid(row=0, column=1)

        ttk.Button(self.frame_formulario_dni, text="Enviar", command=self.buscar_usuario, style='TButton').grid(
            row=1, columnspan=2, sticky=tk.W + tk.E)

    def buscar_usuario(self):
        try:
            documento = self.documento_editar.get()
            # Consultar la información actual del usuario
            query_usuario_actual = 'SELECT * FROM clientes WHERE Dni = ?'
            parametros_usuario_actual = (documento,)
            resultado_usuario_actual = self.run_query(
                query_usuario_actual, parametros_usuario_actual)
            usuario_actual = resultado_usuario_actual.fetchone()
            
            if usuario_actual:
               self.mostrar_formulario_edicion(usuario_actual) 
            else:
                self.message['text'] = 'No existe usuario con ese DNI'
                
        except Exception as e:
            print("Error:", e)

    def mostrar_formulario_edicion(self, usuario_actual):
    # Ocultar el marco principal
        self.limpiar_interfaz()
        self.frame_principal.pack_forget()

        self.frame_formulario_edicion.pack(pady=50, padx=50)

        tk.Label(self.frame_formulario_edicion, text="Nombre: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.nombre = tk.Entry(self.frame_formulario_edicion)
        self.nombre.insert(0, usuario_actual[1])  # Nombre
        self.nombre.grid(row=1, column=1)

        tk.Label(self.frame_formulario_edicion, text="Apellido: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=2, column=0)
        self.apellido = tk.Entry(self.frame_formulario_edicion)
        self.apellido.insert(0, usuario_actual[2])  # Apellido
        self.apellido.grid(row=2, column=1)

        tk.Label(self.frame_formulario_edicion, text="Documento: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=3, column=0)
        self.documento = tk.Entry(self.frame_formulario_edicion)
        self.documento.insert(0, usuario_actual[3])  # DNI
        self.documento.grid(row=3, column=1)

        tk.Label(self.frame_formulario_edicion, text="Plan: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=4, column=0)
        self.Plan = tk.Entry(self.frame_formulario_edicion)
        self.Plan.insert(0, usuario_actual[6])  # Plan
        self.Plan.grid(row=4, column=1)

        ttk.Button(self.frame_formulario_edicion, text="Leer tarjeta", command=self.Leer_tarjeta,
               style='TButton').grid(row=5, columnspan=2, sticky=tk.W+tk.E)
        ttk.Button(self.frame_formulario_edicion, text="Guardar cambios", command=self.guardar_edit,
               style='TButton').grid(row=6, columnspan=2, sticky=tk.W+tk.E)

        self.message = tk.Label(text='', fg='red', font=('Helvetica', 12, 'italic'), bg='#FFA07A')
        self.message.grid(row=7, column=0, columnspan=3, sticky=tk.W + tk.E)

    def validar_edit(self):
        return len(self.nombre.get()) != 0 and len(self.apellido.get()) != 0 and len(self.documento.get()) != 0

    def guardar_edit(self):
        try:
            dni = self.documento.get()


            # Verificar si el DNI ya existe en la base de datos
            query_verificacion = 'SELECT * FROM clientes WHERE Dni = ?'
            parametros_verificacion = (dni,)
            resultado_verificacion = self.run_query(
                query_verificacion, parametros_verificacion)

            if resultado_verificacion.fetchone():
                # El DNI ya existe, realizar edición
                if self.validar_edit():
                    # Obtener la información actualizada
                    nuevo_nombre = self.nombre.get()
                    nuevo_apellido = self.apellido.get()
                    nuevo_plan = self.Plan.get()
                    if not self.validar_plan(nuevo_plan):
                        self.message['text'] = 'Ingrese un plan válido (2-6)'
                        return
                    # Actualizar la base de datos
                    query_actualizar = 'UPDATE clientes SET Nombre = ?, Apellido = ?, Plan = ? WHERE Dni = ?'
                    parametros_actualizar = (nuevo_nombre, nuevo_apellido, nuevo_plan, dni )
                    self.run_query(query_actualizar, parametros_actualizar)

                    self.message['text'] = 'Usuario editado correctamente'
                    self.limpiar_interfaz()

                else:
                    self.message['text'] = 'Un campo está vacío'
            else:
                self.message['text'] = 'Existe usuario con ese DNI'

        except Exception as e:
            print("Error:", e)

    def mostrar_agregar_desde_dni(self):
        # Ocultar el formulario de DNI
        self.frame_formulario_dni.pack_forget()

        # Mostrar el marco de agregar usuarios
        self.frame_agregar_usuarios.pack(pady=50, padx=50)

        # Resto del código de mostrar_agregar()

    def mostrar_formulario_eliminar(self):
        # Ocultar el marco principal
        self.frame_principal.pack_forget()

        # Mostrar el formulario para ingresar el DNI
        self.frame_formulario_eliminar = ttk.Frame(self.root)
        self.frame_formulario_eliminar.pack(pady=50, padx=50)

        tk.Label(self.frame_formulario_eliminar, text="Ingrese DNI a Eliminar: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=0, column=0)
        self.dni_eliminar = tk.Entry(self.frame_formulario_eliminar)
        self.dni_eliminar.focus()
        self.dni_eliminar.grid(row=0, column=1)

        ttk.Button(self.frame_formulario_eliminar, text="Eliminar", command=self.limpiar_interfaz, style='TButton').grid(
            row=1, columnspan=2, sticky=tk.W + tk.E)

    def limpiar_interfaz(self):
        # Limpiar el formulario de agregar usuarios
        self.frame_agregar_usuarios.pack_forget()
        self.frame_formulario_edicion.pack_forget()
        

        # Limpiar el formulario de DNI
        if hasattr(self, 'frame_formulario_dni'):
            self.frame_formulario_dni.pack_forget()

        # Limpiar el formulario de Eliminar
        if hasattr(self, 'frame_formulario_eliminar'):
            self.frame_formulario_eliminar.pack_forget()

        # Volver a mostrar el marco principal
        self.frame_principal.pack(pady=50, padx=50)
        

    def entrar_tarjeta(self):
        # Lógica para el botón "Tarjeta"
        pass

    def mostrar_formulario_dni_ingreso_documento(self):
        # Ocultar el marco principal
        self.frame_principal.pack_forget()

        # Mostrar el formulario para ingresar el DNI
        self.frame_formulario_dni_ingreso_documento = ttk.Frame(self.root)
        self.frame_formulario_dni_ingreso_documento.pack(pady=50, padx=50)

        tk.Label(self.frame_formulario_dni_ingreso_documento, text="Ingrese DNI para Ingreso de Documento: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=0, column=0)
        self.dni_ingreso_documento = tk.Entry(self.frame_formulario_dni_ingreso_documento)
        self.dni_ingreso_documento.focus()
        self.dni_ingreso_documento.grid(row=0, column=1)

        ttk.Button(self.frame_formulario_dni_ingreso_documento, text="Ingresar", command=self.ingreso_documento_desde_dni, style='TButton').grid(
            row=1, columnspan=2, sticky=tk.W + tk.E)

    def ingreso_documento_desde_dni(self):
        # Ocultar el formulario de DNI para ingreso de documento
        self.frame_formulario_dni_ingreso_documento.pack_forget()

        # Lógica para ingreso de documento (puedes adaptarla según tus necesidades)
        dni_ingresado = self.dni_ingreso_documento.get()
        # Aquí deberías incluir la lógica específica para ingreso de documento usando el DNI ingresado

        # Volver a mostrar el marco principal
        self.frame_principal.pack(pady=50, padx=50)

    def mostrar_formulario_dni_sumar_mes(self):
        # Ocultar el marco principal
        self.frame_principal.pack_forget()

        # Mostrar el formulario para ingresar el DNI
        self.frame_formulario_dni_sumar_mes = ttk.Frame(self.root)
        self.frame_formulario_dni_sumar_mes.pack(pady=50, padx=50)

        tk.Label(self.frame_formulario_dni_sumar_mes, text="Ingrese DNI para Sumar Mes: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=0, column=0)
        self.dni_sumar_mes = tk.Entry(self.frame_formulario_dni_sumar_mes)
        self.dni_sumar_mes.focus()
        self.dni_sumar_mes.grid(row=0, column=1)

        ttk.Button(self.frame_formulario_dni_sumar_mes, text="Enviar", command=self.sumar_mes_desde_dni, style='TButton').grid(
            row=1, columnspan=2, sticky=tk.W + tk.E)

    def sumar_mes_desde_dni(self):
        # Ocultar el formulario de DNI para sumar mes
        self.frame_formulario_dni_sumar_mes.pack_forget()

        # Lógica para sumar el mes (puedes adaptarla según tus necesidades)
        # Aquí deberías incluir la lógica específica para sumar el mes usando el DNI ingresado

        # Volver a mostrar el marco principal
        self.frame_principal.pack(pady=50, padx=50)

    def exportar_a_excel(self):
        # Lógica para el botón "excel"
        pass



if __name__ == "__main__":
    root = tk.Tk()
    app = Acceso(root)
    root.mainloop()
