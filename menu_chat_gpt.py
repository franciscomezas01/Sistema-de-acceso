from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QGridLayout, QGroupBox, QStyleFactory
import sqlite3
import datetime
import pandas as pd
import serial


class Acceso(QMainWindow):
    db_name = 'acceso.db'

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Gimnasio {Nombre}')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.style = QStyleFactory.create('Fusion')
        QApplication.setStyle(self.style)

        grid_layout = QGridLayout(central_widget)

        frame_principal = QGroupBox('Principal')
        grid_layout.addWidget(frame_principal, 0, 0)

        frame_agregar = self.create_group_box("Usuario")
        grid_layout.addWidget(frame_agregar, 0, 0)

        frame_leer = self.create_group_box("Ingreso")
        grid_layout.addWidget(frame_leer, 0, 1)

        frame_sumar_mes = self.create_group_box("Sumar Mes")
        grid_layout.addWidget(frame_sumar_mes, 1, 1)

        frame_excel = self.create_group_box("Exportar")
        grid_layout.addWidget(frame_excel, 1, 0)

        self.show()

    def create_group_box(self, title):
        group_box = QGroupBox(title)
        vbox = QVBoxLayout()

        if title == "Usuario":
            vbox.addWidget(QPushButton('Agregar', clicked=self.agregar_usuario))
            vbox.addWidget(QPushButton('Eliminar', clicked=self.eliminar_usuario))
            vbox.addWidget(QPushButton('Actualizar datos', clicked=self.actualizar_datos))
        elif title == "Ingreso":
            vbox.addWidget(QPushButton('Tarjeta', clicked=self.leer_tarjeta))
            vbox.addWidget(QPushButton('Documento', clicked=self.ingreso_dni))
        elif title == "Sumar Mes":
            vbox.addWidget(QPushButton('Sumar Mes', clicked=self.sumar_mes))
            vbox.addWidget(QPushButton('Sumar 6 Meses', clicked=self.sumar_6mes))
            vbox.addWidget(QPushButton('Sumar un Anio', clicked=self.sumar_anio))
            vbox.addWidget(QPushButton('Sumar 66 Meses', clicked=self.sumar_66mes))  # Nueva función
        elif title == "Exportar":
            vbox.addWidget(QPushButton('Excel', clicked=self.exportar_a_excel))

        group_box.setLayout(vbox)
        return group_box

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parameters)
            conn.commit()
        return resultado

    def agregar_usuario(self):
        try:
            dni = input("Ingrese el DNI del cliente: ")

            if dni:
                query_verificacion = 'SELECT * FROM clientes WHERE Dni = ?'
                parametros_verificacion = (dni,)
                resultado_verificacion = self.run_query(query_verificacion, parametros_verificacion)

                if resultado_verificacion.fetchone():
                    print('El DNI ya existe en la base de datos')
                else:
                    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
                    tarjeta_id = "8675309125"
                    query = 'INSERT INTO clientes (Nombre, Apellido, Dni, Tarjeta, Fecha) VALUES (?, ?, ?, ?, ?)'
                    parametros = (input("Ingrese el nombre del cliente: "),
                                  input("Ingrese el apellido del cliente: "),
                                  dni, tarjeta_id, fecha_actual)
                    self.run_query(query, parametros)
                    print("Usuario guardado en la base de datos.")

        except Exception as e:
            print("Error:", e)

    def eliminar_usuario(self):
        try:
            dni = input("Ingrese el DNI del cliente a eliminar: ")

            if dni:
                query = 'DELETE FROM clientes WHERE Dni = ?'
                parametros = (dni,)
                self.run_query(query, parametros)
                print(f'Se ha eliminado al cliente con DNI {dni}')
            else:
                print('Ingrese un DNI válido')

        except Exception as e:
            print("Error:", e)

    def actualizar_datos(self):
        try:
            dni = input("Ingrese el DNI del cliente a actualizar: ")

            if dni:
                query = 'SELECT * FROM clientes WHERE Dni = ?'
                parametros = (dni,)
                resultado = self.run_query(query, parametros)

                if resultado.fetchone():
                    nuevos_datos = {
                        'Nombre': input("Ingrese el nuevo nombre del cliente: "),
                        'Apellido': input("Ingrese el nuevo apellido del cliente: "),
                    }

                    query_actualizar = 'UPDATE clientes SET Nombre = ?, Apellido = ? WHERE Dni = ?'
                    parametros_actualizar = (nuevos_datos['Nombre'], nuevos_datos['Apellido'], dni)
                    self.run_query(query_actualizar, parametros_actualizar)
                    print(f'Datos actualizados para el cliente con DNI {dni}')
                else:
                    print(f'No existe cliente con el DNI {dni}')

            else:
                print('Ingrese un DNI válido')

        except Exception as e:
            print("Error:", e)

    def leer_tarjeta(self):
        try:
            ser = serial.Serial('COM3', 9600)
            tarjeta_id = ser.readline().decode().strip()
            ser.close()

            self.tarjeta_id = tarjeta_id
            print("ID de tarjeta: ", tarjeta_id)

        except Exception as e:
            print("error:", e)

    def ingreso_dni(self):
        try:
            documento = input("Ingrese el DNI del cliente: ")
            fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

            dni_existente_query = 'SELECT * FROM clientes WHERE Dni = ?'
            dni_existente_parametros = (documento,)
            dni_existente_resultado = self.run_query(dni_existente_query, dni_existente_parametros)

            if dni_existente_resultado.fetchone():
                query = 'SELECT * FROM clientes WHERE Dni = ? AND date(Fecha) < date(?)'
                parametros = (documento, fecha_actual)
                resultado = self.run_query(query, parametros)

                if resultado.fetchone():
                    print('Paga la cuota rata')
                else:
                    print('BIENVENIDO')

            else:
                print('No existe usuario con ese DNI')

        except Exception as e:
            print("Error:", e)

    def sumar_mes(self):
        try:
            documento = input("Ingrese el DNI del cliente para sumar un mes: ")

            if documento:
                query = 'UPDATE clientes SET Fecha = DATE(Fecha, "+1 month") WHERE Dni = ?'
                parametros = (documento,)
                self.run_query(query, parametros)
                print(f'Se ha sumado un mes al cliente con DNI {documento}')
            else:
                print('Ingrese un DNI válido')

        except Exception as e:
            print("Error:", e)

    def sumar_6mes(self):
        try:
            documento = input("Ingrese el DNI del cliente para sumar 6 meses: ")

            if documento:
                query = 'UPDATE clientes SET Fecha = DATE(Fecha, "+6 month") WHERE Dni = ?'
                parametros = (documento,)
                self.run_query(query, parametros)
                print(f'Se han sumado 6 meses al cliente con DNI {documento}')
            else:
                print('Ingrese un DNI válido')

        except Exception as e:
            print("Error:", e)

    def sumar_anio(self):
        try:
            documento = input("Ingrese el DNI del cliente para sumar un año: ")

            if documento:
                query = 'UPDATE clientes SET Fecha = DATE(Fecha, "+12 month") WHERE Dni = ?'
                parametros = (documento,)
                self.run_query(query, parametros)
                print(f'Se ha sumado un año al cliente con DNI {documento}')
            else:
                print('Ingrese un DNI válido')

        except Exception as e:
            print("Error:", e)

    def sumar_66mes(self):
        try:
            documento = input("Ingrese el DNI del cliente para sumar 66 meses: ")

            if documento:
                query = 'UPDATE clientes SET Fecha = DATE(Fecha, "+66 month") WHERE Dni = ?'
                parametros = (documento,)
                self.run_query(query, parametros)
                print(f'Se han sumado 66 meses al cliente con DNI {documento}')
            else:
                print('Ingrese un DNI válido')

        except Exception as e:
            print("Error:", e)

    def exportar_a_excel(self):
        try:
            query = 'SELECT * FROM clientes'

            with sqlite3.connect(self.db_name) as conn:
                df = pd.read_sql_query(query, conn)

            df.to_excel('datos_clientes.xlsx', index=False)
            print("Datos exportados a Excel exitosamente.")

        except Exception as e:
            print("Error al exportar a Excel:", e)


if __name__ == '__main__':
    app = QApplication([])
    ventana = Acceso()
    app.exec_()
