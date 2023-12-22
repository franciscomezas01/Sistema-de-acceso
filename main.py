from tkinter import ttk
from tkinter import *
import sqlite3
import serial
import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd


class Acceso:

    db_name = 'acceso.db'

    def __init__(self, ventana):
        self.wind = ventana
        self.wind.title('Gimnasio {Nombre}')
        self.wind.configure(bg='#7D3C98')

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12))

        # Marco principal
        # Fondo en color LightSalmon
        frame_principal = Frame(self.wind, bg='#A569BD')
        frame_principal.grid(row=0, column=0, pady=50, padx=50)

        # Marco para agregar usuario
        frame_agregar = LabelFrame(frame_principal, text="Usuario", font=(
            'Helvetica', 14, 'bold'), bg='#5499C7')
        frame_agregar.grid(row=0, column=0, pady=20, padx=10)
        ttk.Button(frame_agregar, text='Agregar', command=self.agregar_usuario,
                   style='TButton').grid(row=0, column=0,  padx=10, sticky=W+E, columnspan=2)
        ttk.Button(frame_agregar, text='Eliminar', command=self.eliminar_usuario,
                   style='TButton').grid(row=1, column=0,  padx=10, sticky=W+E, columnspan=2)
        ttk.Button(frame_agregar, text='Actualizar datos', command=self.editar,
                   style='TButton').grid(row=2, column=0,  padx=10, sticky=W+E, columnspan=2)

        # Marco para leer tarjetas
        frame_leer = LabelFrame(frame_principal, text="Ingreso", font=(
            'Helvetica', 14, 'bold'), bg='#5499C7')
        frame_leer.grid(row=0, column=1, pady=20, padx=10)
        ttk.Button(frame_leer, text='Tarjeta',command=self.entrar_tarjeta, style='TButton').grid(
            row=0, column=0, sticky=W+E)
        ttk.Button(frame_leer, text='Documento', command=self.ingreso_dni,
                   style='TButton').grid(row=1, column=0, sticky=W+E)

        # Marco para sumar mes
        frame_sumar_mes = LabelFrame(frame_principal, text="Sumar", font=(
            'Helvetica', 14, 'bold'), bg='#5499C7')
        frame_sumar_mes.grid(row=1, column=1, pady=20, padx=10)
        ttk.Button(frame_sumar_mes, text='Sumar mes', command=lambda:self.sumar_mes(1),
                   style='TButton').grid(row=0, column=0, sticky=W+E)
        ttk.Button(frame_sumar_mes, text='Sumar 6 meses', command=lambda:self.sumar_mes(6),
                   style='TButton').grid(row=1, column=0, sticky=W+E)
        ttk.Button(frame_sumar_mes, text='Sumar un año', command=lambda:self.sumar_mes(12),
                   style='TButton').grid(row=2, column=0, sticky=W+E)

        frame_excel = LabelFrame(frame_principal, text="Exportar", font=(
            'Helvetica', 14, 'bold'), bg='#5499C7')
        frame_excel.grid(row=1, column=0, pady=20, padx=10)
        ttk.Button(frame_excel, text='excel', command=self.exportar_a_excel,
                   style='TButton').grid(row=0, column=0, sticky=W+E)

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parameters)
            conn.commit()
        return resultado

    def agregar_usuario(self):
        self.ventana_usuario = Toplevel()
        self.ventana_usuario.title('Agregar usuario')
        self.ventana_usuario.configure(bg='#FFA07A')

        Label(self.ventana_usuario, text="Nombre: ", font=(
            'Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.nombre = Entry(self.ventana_usuario)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        Label(self.ventana_usuario, text="Apellido: ", font=(
            'Helvetica', 12), bg='#FFA07A').grid(row=2, column=0)
        self.apellido = Entry(self.ventana_usuario)
        self.apellido.grid(row=2, column=1)

        Label(self.ventana_usuario, text="Documento: ", font=(
            'Helvetica', 12), bg='#FFA07A').grid(row=3, column=0)
        self.documento = Entry(self.ventana_usuario)
        self.documento.grid(row=3, column=1)
        
        Label(self.ventana_usuario, text="Plan(2-6): ", font=(
            'Helvetica', 12), bg='#FFA07A').grid(row=4, column=0)
        self.Plan = Entry(self.ventana_usuario)
        self.Plan.grid(row=4, column=1)

        ttk.Button(self.ventana_usuario, text="Leer tarjeta", command=self.Leer_tarjeta,
                   style='TButton').grid(row=5, columnspan=2, sticky=W+E)
        ttk.Button(self.ventana_usuario, text="Guardar usuario", command=self.guardar_usuario,
                   style='TButton').grid(row=6, columnspan=2, sticky=W+E)

        self.message = Label(text='', fg='red', font=(
            'Helvetica', 12, 'italic'), bg='#FFA07A')  # Fondo en color LightSalmon
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)


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
            elif self.validacion():
                fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
                #En caso de no tener arduino se puede descomentar esta linea y sacarle el self a la tarjeta para verificar almacenamiento
                tarjeta_id = "8675309125" 
                query = 'INSERT INTO clientes (Nombre, Apellido, Dni, Tarjeta, Fecha, Plan ) VALUES (?, ?, ?, ?, ?, ?)'
                parametros = (self.nombre.get(), self.apellido.get(
                ), dni, tarjeta_id, fecha_actual, plan)
                self.run_query(query, parametros)

                print("Usuario guardado en la base de datos.")
                self.message['text'] = 'El cliente {} fue agregado'.format(
                    self.nombre.get())
                self.nombre.delete(0, END)
                self.apellido.delete(0, END)
                self.documento.delete(0, END)

                self.ventana_usuario.destroy()
            else:
                print("campos vacíos")
                self.message['text'] = 'Un campo está vacío'

        except Exception as e:
            print("Error:", e)
    
    def editar(self):
        self.ventana_Editar = Toplevel()
        self.ventana_Editar.title('Editar usuario')
        self.ventana_Editar.configure(bg='#FFA07A')

        Label(self.ventana_Editar, text="Documento: ", font=(
            'Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.documento_editar = Entry(self.ventana_Editar)
        self.documento_editar.focus()
        self.documento_editar.grid(row=1, column=1)

        ttk.Button(self.ventana_Editar, text="Buscar usuario", command=self.buscar_usuario,
                   style='TButton').grid(row=6, columnspan=2, sticky=W+E)
        self.message = Label(text='', fg='red', font=(
            'Helvetica', 12, 'italic'), bg='#FFA07A')
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)

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
                # Rellenar los campos de edición con la información actual
                self.ventana_usuario = Toplevel()
                self.ventana_usuario.title('Editar usuario')
                self.ventana_usuario.configure(bg='#FFA07A')

                Label(self.ventana_usuario, text="Nombre: ", font=(
                    'Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
                self.nombre = Entry(self.ventana_usuario)
                self.nombre.insert(0, usuario_actual[1])  # Nombre
                self.nombre.grid(row=1, column=1)

                Label(self.ventana_usuario, text="Apellido: ", font=(
                    'Helvetica', 12), bg='#FFA07A').grid(row=2, column=0)
                self.apellido = Entry(self.ventana_usuario)
                self.apellido.insert(0, usuario_actual[2])  # Apellido
                self.apellido.grid(row=2, column=1)

                Label(self.ventana_usuario, text="Documento: ", font=(
                    'Helvetica', 12), bg='#FFA07A').grid(row=3, column=0)
                self.documento = Entry(self.ventana_usuario)
                self.documento.insert(0, usuario_actual[3])  # DNI
                self.documento.grid(row=3, column=1)

                ttk.Button(self.ventana_usuario, text="Leer tarjeta", command=self.Leer_tarjeta,
                           style='TButton').grid(row=5, columnspan=2, sticky=W+E)
                ttk.Button(self.ventana_usuario, text="Guardar cambios", command=self.guardar_edit,
                           style='TButton').grid(row=6, columnspan=2, sticky=W+E)

                self.message = Label(text='', fg='red', font=(
                    'Helvetica', 12, 'italic'), bg='#FFA07A')
                self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)

            else:
                self.message['text'] = 'No existe usuario con ese DNI'

        except Exception as e:
            print("Error:", e)

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

                    # Actualizar la base de datos
                    query_actualizar = 'UPDATE clientes SET Nombre = ?, Apellido = ? WHERE Dni = ?'
                    parametros_actualizar = (nuevo_nombre, nuevo_apellido, dni)
                    self.run_query(query_actualizar, parametros_actualizar)

                    self.message['text'] = 'Usuario editado correctamente'
                    self.ventana_usuario.destroy()
                    self.ventana_Editar.destroy()
                else:
                    self.message['text'] = 'Un campo está vacío'
            else:
                self.message['text'] = 'No existe usuario con ese DNI'

        except Exception as e:
            print("Error:", e)

    
    def eliminar_usuario(self):
        self.ventana_Borrar = Toplevel()
        self.ventana_Borrar.title('Eliminar usuario')
        self.ventana_Borrar.configure(bg='#FFA07A')

        Label(self.ventana_Borrar, text="Documento: ", font=(
            'Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.documento = Entry(self.ventana_Borrar)
        self.documento.focus()
        self.documento.grid(row=1, column=1)

        ttk.Button(self.ventana_Borrar, text="Eliminar usuario", command=self.borrar,
                   style='TButton').grid(row=6, columnspan=2, sticky=W+E)
        self.message = Label(text='', fg='red', font=(
            'Helvetica', 12, 'italic'), bg='#FFA07A')
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)
    
    def borrar(self):
        try:
            documento = self.documento.get()
            if documento:
                query = 'DELETE FROM clientes WHERE dni = ?'
                parametros = (documento,)
                self.run_query(query, parametros)
                self.message['text'] = 'Se ha eliminado al cliente con documento {}'.format(documento)
                self.ventana_Borrar.destroy()
            else:
                self.message['text'] = 'Ingrese un documento válido'

        except Exception as e:
            print("Error:", e)    
    
    def sumar_mes(self,cantidad_meses):
        self.ventana_mes = Toplevel()
        self.ventana_mes.title('Abono de cuota')
        self.ventana_mes.configure(bg='#FFA07A')

        Label(self.ventana_mes, text="Documento: ", font=(
            'Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.documento = Entry(self.ventana_mes)
        self.documento.focus()
        self.documento.grid(row=1, column=1)
        self.cantidad_meses = cantidad_meses

        ttk.Button(self.ventana_mes, text="Abonar cuota", command=self.mes,
                   style='TButton').grid(row=6, columnspan=2, sticky=W+E)
        self.message = Label(text='', fg='red', font=(
            'Helvetica', 12, 'italic'), bg='#FFA07A')
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)


    def mes(self):
        try:
            documento = self.documento.get()
            if documento:
                query = 'UPDATE clientes SET Fecha = DATE(Fecha, "+{} month") WHERE Dni = ?'.format(self.cantidad_meses)
                parametros = (documento,)
                self.run_query(query, parametros)
                self.message['text'] = 'Se ha sumado {} mes al cliente con documento {}'.format(
                   self.cantidad_meses, documento)
                self.ventana_mes.destroy()
            else:
                self.message['text'] = 'Ingrese un documento válido'

        except Exception as e:
            print("Error:", e)

    def ingreso_dni(self):
        self.ventana_dni = Toplevel()
        self.ventana_dni.title('Ingreso por dni')
        self.ventana_dni.configure(bg='#FFA07A')

        Label(self.ventana_dni, text="Documento: ", font=(
            'Helvetica', 12), bg='#FFA07A').grid(row=1, column=0)
        self.documento = Entry(self.ventana_dni)
        self.documento.focus()
        self.documento.grid(row=1, column=1)

        ttk.Button(self.ventana_dni, text="Ingresar", command=self.verificacion_dni,
                   style='TButton').grid(row=6, columnspan=2, sticky=W+E)
        self.message = Label(text='', fg='red', font=(
            'Helvetica', 12, 'italic'), bg='#FFA07A')
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)

    def verificacion_dni(self):
        try:
            puerto_serial = "COM3"  
            baud_rate = 9600 
            ser = serial.Serial(puerto_serial, baud_rate, timeout=1)
            documento = self.documento.get()
            fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
            dni_existente_query = 'SELECT * FROM clientes WHERE Dni = ?'
            dni_existente_parametros = (documento,)
            dni_existente_resultado = self.run_query(
                dni_existente_query, dni_existente_parametros)
            if dni_existente_resultado.fetchone():
                query = 'SELECT * FROM clientes WHERE Dni = ? AND date(Fecha) < date(?)'
                parametros = (documento, fecha_actual)
                resultado = self.run_query(query, parametros)

                if resultado.fetchone():

                    self.message['text'] = 'Paga la cuota rata'
                    ser.write(b'0')
                else:
                    self.message['text'] = 'BIENVENIDO'
                    ser.write(b'1')

                self.ventana_dni.destroy()
            else:
                self.message['text'] = 'No existe usuario con ese dni'
        except Exception as e:
            print("Error:", e)

    def exportar_a_excel(self):
        try:
            # consulta SQL para obtenedatos
            query = 'SELECT * FROM clientes'

            # datos de la base de datos
            with sqlite3.connect(self.db_name) as conn:
                df = pd.read_sql_query(query, conn)

            df.to_excel('datos_clientes.xlsx', index=False)
            print("Datos exportados a Excel exitosamente.")

        except Exception as e:
            print("Error al exportar a Excel:", e)

    def entrar_tarjeta(self):
        fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
        arduino_port = 'COM3'
        ser = serial.Serial(arduino_port, 9600, timeout=1)
        self.message = Label(text='', fg='red', font=(
            'Helvetica', 12, 'italic'), bg='#FFA07A')
        self.message.grid(row=7, column=0, columnspan=3, sticky=W + E)
        while True:
        # Lee la línea recibida desde Arduino
            tarjeta_id = ser.readline().decode('utf-8').rstrip()
        
            if tarjeta_id:
                print("id de tarjeta", tarjeta_id)
                self.tarjeta_id = tarjeta_id
                break   
        tarj_exis_query = 'SELECT * FROM clientes WHERE Tarjeta = ?' 
        tarj_exis_parametros = (tarjeta_id,)
        tarjeta_existente_resultado = self.run_query(tarj_exis_query,tarj_exis_parametros)   
        if tarjeta_existente_resultado.fetchone():
            query = "SELECT * FROM clientes WHERE Tarjeta = ? AND date(Fecha) < date(?)"
            parametros = (tarjeta_id, fecha_actual)
            resultado = self.run_query(query, parametros)

            if resultado.fetchone():
                print(" NO pude ingreesar correctamente")
                self.message['text'] = 'Paga la cuota rata'
                ser.write(b'0')
            else:
                self.message['text'] = 'BIENVENIDO'
                ser.write(b'1')
                print("pude ingresar correctamente")
                
        else:   
            self.message['text'] = 'Usuario no existente'
            ser.write(b'2')


if __name__ == '__main__':
    ventana = Tk()
    aplicacion = Acceso(ventana)
    ventana.mainloop()
