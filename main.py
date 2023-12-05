from tkinter import ttk
from tkinter import *
import sqlite3
import serial
import datetime

import pandas as pd

class Acceso:

    db_name = 'acceso.db'

    def __init__(self, ventana):
        self.wind = ventana
        self.wind.title('Gimnasio {Nombre}')  # Reemplaza {Nombre} con el nombre de tu gimnasio
        self.wind.configure(bg='#7D3C98')  # Fondo en color LightSalmon

        # Estilo de los botones
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12))

        # Marco principal
        frame_principal = Frame(self.wind, bg='#A569BD')  # Fondo en color LightSalmon
        frame_principal.grid(row=0, column=0, pady=50, padx=50)

        # Marco para agregar usuario
        frame_agregar = LabelFrame(frame_principal, text="Agregar usuario", font=('Helvetica', 14, 'bold'), bg='#5499C7')
        frame_agregar.grid(row=0, column=0, pady=20, padx=10)
        ttk.Button(frame_agregar, text='Usuarios', command=self.agregar_usuario, style='TButton').grid(row=1, column=0,  padx=10, sticky=W+E, columnspan=2)

        # Marco para leer tarjetas
        frame_leer = LabelFrame(frame_principal, text="Leer tarjetas", font=('Helvetica', 14, 'bold'), bg='#5499C7')
        frame_leer.grid(row=0, column=1, pady=20, padx=10)
        ttk.Button(frame_leer, text='Acceso', command=self.agregar_usuario, style='TButton').grid(row=0, column=0, sticky=W+E)

        # Marco para ingreso por DNI
        frame_dni = LabelFrame(frame_principal, text="Ingreso por DNI", font=('Helvetica', 14, 'bold'), bg='#5499C7')
        frame_dni.grid(row=1, column=0, pady=20, padx=10)
        ttk.Button(frame_dni, text='Documento', command=self.ingreso_dni, style='TButton').grid(row=0, column=0, sticky=W+E)

        # Marco para sumar mes
        frame_sumar_mes = LabelFrame(frame_principal, text="Sumar Mes", font=('Helvetica', 14, 'bold'), bg='#5499C7')
        frame_sumar_mes.grid(row=1, column=1, pady=20, padx=10)
        ttk.Button(frame_sumar_mes, text='Sumar', command=self.sumar_mes, style='TButton').grid(row=0, column=0, sticky=W+E)

        frame_excel = LabelFrame(frame_principal, text="Exportar", font=('Helvetica', 14, 'bold'), bg='#5499C7')
        frame_excel.grid(row=2, column=0, pady=20, padx=10)
        ttk.Button(frame_excel, text='excel', command=self.exportar_a_excel, style='TButton').grid(row=0, column=0, sticky=W+E)

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parameters)
            conn.commit()
        return resultado

    def agregar_usuario(self):
        self.ventana_usuario = Toplevel()
        self.ventana_usuario.title('Agregar usuario')
        self.ventana_usuario.configure(bg='#FFA07A')  # Fondo en color LightSalmon

        Label(self.ventana_usuario, text="Nombre: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.nombre = Entry(self.ventana_usuario)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        Label(self.ventana_usuario, text="Apellido: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=2, column=0)
        self.apellido = Entry(self.ventana_usuario)
        self.apellido.grid(row=2, column=1)

        Label(self.ventana_usuario, text="Documento: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=3, column=0)
        self.documento = Entry(self.ventana_usuario)
        self.documento.grid(row=3, column=1)

        ttk.Button(self.ventana_usuario, text="Leer tarjeta", command=self.Leer_tarjeta, style='TButton').grid(row=5, columnspan=2, sticky=W+E)
        ttk.Button(self.ventana_usuario, text="Guardar usuario", command=self.guardar_usuario, style='TButton').grid(row=6, columnspan=2, sticky=W+E)

        self.message = Label(text='', fg='red', font=('Helvetica', 12, 'italic'), bg='#FFA07A')  # Fondo en color LightSalmon
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)

    def Leer_tarjeta(self):
        try:
            ser = serial.Serial('COM3', 9600)
            tarjeta_id = ser.readline().decode().strip()
            ser.close()

        except Exception as e:
            print("error:", e)

        self.tarjeta_id = tarjeta_id
        print("ID de tarjeta: ", tarjeta_id)

    def validacion(self):
        return len(self.nombre.get()) != 0 and len(self.apellido.get()) != 0 and len(self.documento.get()) != 0

    def guardar_usuario(self):
        try:
            if self.validacion():
                fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
                tarjeta_id = "8675309125"
                query = 'INSERT INTO clientes (Nombre, Apellido, Dni, Tarjeta, Fecha) VALUES (?, ?, ?, ?, ?)'
                parametros = (self.nombre.get(), self.apellido.get(), self.documento.get(), tarjeta_id, fecha_actual)
                self.run_query(query, parametros)

                print("Usuario guardado en la base de datos.")
                self.message['text'] = 'El cliente {} fue agregado'.format(self.nombre.get())
                self.nombre.delete(0, END)
                self.apellido.delete(0, END)
                self.documento.delete(0, END)

                self.ventana_usuario.destroy()
            else:
                print("campos vacíos")
                self.message['text'] = 'Un campo está vacío'

        except Exception as e:
            print("Error:", e)

    def sumar_mes(self):
        self.ventana_mes = Toplevel()
        self.ventana_mes.title('Abono de cuota')
        self.ventana_mes.configure(bg='#FFA07A')  # Fondo en color LightSalmon

        Label(self.ventana_mes, text="Documento: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.documento = Entry(self.ventana_mes)
        self.documento.focus()
        self.documento.grid(row=1, column=1)

        ttk.Button(self.ventana_mes, text="Abonar cuota", command=self.mes, style='TButton').grid(row=6, columnspan=2, sticky=W+E)

        self.message = Label(text='Se guardo la cuota', fg='red', font=('Helvetica', 12, 'italic'), bg='#FFA07A')  # Fondo en color LightSalmon
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)
        
    def mes(self):
        try:
            documento = self.documento.get()
            
            if documento:
                query = 'UPDATE clientes SET Fecha = DATE(Fecha, "+1 month") WHERE Dni = ?'
                parametros = (documento,)
                self.run_query(query, parametros)
                self.message['text'] = 'Se ha sumado un mes al cliente con documento {}'.format(documento)
                self.ventana_mes.destroy()
            else:
                self.message['text'] = 'Ingrese un documento válido'

        except Exception as e:
            print("Error:", e)
            
    def ingreso_dni(self):
        self.ventana_dni = Toplevel()
        self.ventana_dni.title('Ingreso por dni')
        self.ventana_dni.configure(bg='#FFA07A')  # Fondo en color LightSalmon

        Label(self.ventana_dni, text="Documento: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.documento = Entry(self.ventana_dni)
        self.documento.focus()
        self.documento.grid(row=1, column=1)

        ttk.Button(self.ventana_dni, text="Ingresar", command=self.verificacion_dni, style='TButton').grid(row=6, columnspan=2, sticky=W+E)
        self.message = Label(text='', fg='red', font=('Helvetica', 12, 'italic'), bg='#FFA07A')  # Fondo en color LightSalmon
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)
        
    def verificacion_dni(self):
        try:
            documento = self.documento.get()
            # Obtener la fecha actual en el formato correcto para SQLite
            fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

            query = 'SELECT * FROM clientes WHERE Dni = ? AND date(Fecha) < date(?)'
            parametros = (documento, fecha_actual)
            resultado = self.run_query(query, parametros)

            # Verificar si hay resultados (si la fecha almacenada es menor que la fecha actual)
            if resultado.fetchone():
                self.message['text'] = 'Paga la cuota rata'
            else:
                self.message['text'] = 'BIENVENIDO'
                
            self.ventana_dni.destroy()    

        except Exception as e:
            print("Error:", e)
    
    def exportar_a_excel(self):
        try:
            # Consulta SQL para obtener todos los datos de la tabla clientes
            query = 'SELECT * FROM clientes'
            
            # Obtener los datos de la base de datos
            with sqlite3.connect(self.db_name) as conn:
                df = pd.read_sql_query(query, conn)

            # Guardar el DataFrame en un archivo Excel
            df.to_excel('datos_clientes.xlsx', index=False)
            print("Datos exportados a Excel exitosamente.")

        except Exception as e:
            print("Error al exportar a Excel:", e)
            
if __name__ == '__main__':
    ventana = Tk()
    aplicacion = Acceso(ventana)
    ventana.mainloop()
