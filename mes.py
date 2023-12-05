import sqlite3
from datetime import datetime, timedelta
import random

# Conectarse a la base de datos SQLite
conexion = sqlite3.connect('acceso.db')
cursor = conexion.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        dni TEXT,
        tarjeta TEXT,
        fecha TEXT
    )
''')

# Agregar datos de ejemplo si la tabla está vacía
cursor.execute("SELECT COUNT(*) FROM clientes")
if cursor.fetchone()[0] == 0:
    for i in range(1, 6):
        nombre = f"Cliente_{i}"
        apellido = f"Apellido_{i}"
        dni = f"DNI_{i}"
        tarjeta = f"Tarjeta_{i}"
        fecha = f"{random.randint(1, 28)}-12-2023"  # Fecha aleatoria en diciembre de 2023

        cursor.execute("INSERT INTO clientes (nombre, apellido, dni, tarjeta, fecha) VALUES (?, ?, ?, ?, ?)",
                       (nombre, apellido, dni, tarjeta, fecha))

    # Confirmar los cambios
    conexion.commit()

# Menú de opciones
while True:
    print("\nMenú de opciones:")
    print("1. Sumar un mes a la fecha del primer cliente")
    print("2. Mostrar lista de clientes")
    print("0. Salir")

    opcion = input("Ingrese el número de opción: ")

    if opcion == '1':
        # Obtener la fecha actual del primer cliente
        cursor.execute("SELECT id, fecha FROM clientes WHERE id = 1")
        resultado = cursor.fetchone()

        if resultado:
            id_cliente, fecha = resultado

            # Convertir la fecha de string a objeto datetime
            fecha_objeto = datetime.strptime(fecha, '%d-%m-%Y')

            # Sumar un mes a la fecha actual
            nueva_fecha = fecha_objeto + timedelta(days=30)

            # Convertir la nueva fecha de objeto datetime a string
            nueva_fecha_str = nueva_fecha.strftime('%d-%m-%Y')

            # Actualizar la fecha en la base de datos
            cursor.execute("UPDATE clientes SET fecha = ? WHERE id = ?", (nueva_fecha_str, id_cliente))

            # Confirmar los cambios
            conexion.commit()
            print("Fecha actualizada exitosamente.")

    elif opcion == '2':
        # Mostrar lista de clientes
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        if clientes:
            print("\nLista de clientes:")
            for cliente in clientes:
                print(cliente)
        else:
            print("La tabla de clientes está vacía.")

    elif opcion == '0':
        # Salir del programa
        break

# Cerrar la conexión
conexion.close()
