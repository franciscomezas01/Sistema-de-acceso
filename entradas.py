import sqlite3
import datetime

def crear_tabla_registro_entradas():
    conexion = sqlite3.connect('acceso.db')
    cursor = conexion.cursor()

    # Crea la tabla para el registro de entradas
    cursor.execute('''
        CREATE TABLE registro_entradas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            fecha_entrada TEXT,
            hora_entrada TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        );
    ''')

    conexion.commit()
    conexion.close()

def registrar_entrada(cliente_id):
    conexion = sqlite3.connect('tu_basededatos.db')
    cursor = conexion.cursor()

    # Obtiene la fecha y hora actuales
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

    # Inserta una nueva entrada en el registro
    cursor.execute('''
        INSERT INTO registro_entradas (cliente_id, fecha_entrada, hora_entrada)
        VALUES (?, ?, ?);
    ''', (cliente_id, fecha_actual, hora_actual))

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    # Ejecuta esta función una vez para crear la tabla de registro_entradas
    crear_tabla_registro_entradas()

    # Luego, cuando un cliente entra, llama a esta función para registrar la entrada
    # Supongamos que el cliente con ID 1 está entrando
    registrar_entrada(1)
