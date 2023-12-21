# Sistema de Control de Acceso para Gimnasio

Este proyecto implementa un sistema de control de acceso para un gimnasio utilizando una interfaz gráfica desarrollada en Python con la biblioteca Tkinter y una base de datos SQLite para gestionar la información de los usuarios. La comunicación con un dispositivo Arduino se realiza a través del puerto serial para controlar el acceso mediante tarjetas RFID y verificación por documento.

## Requisitos

- Python 3.x
- Bibliotecas Python: tkinter, ttkthemes, sqlite3, pandas, pyserial, datetime, dateutil
- Arduino

## Estructura del Proyecto

- **main.py:** Contiene la clase principal Acceso que gestiona la interfaz gráfica y la lógica del sistema.
- **acceso.db:** Base de datos SQLite para almacenar la información de los usuarios.
- **arduino_access_control.ino:** Código Arduino para controlar el acceso a través del puerto serial.

## Configuración del Entorno

1. Instalar las bibliotecas necesarias:

    ```bash
    pip install -r requirements.txt
    ```

2. Conectar el Arduino y cargar el código arduino_access_control.ino en el dispositivo.

## Ejecución del Programa

Ejecutar main.py para iniciar la aplicación. La interfaz proporcionará opciones para agregar, eliminar y editar usuarios, controlar el acceso mediante tarjeta o documento, y exportar datos a un archivo Excel.

## Funcionalidades Adicionales

- **Agregar y Editar Usuario:** Se puede ingresar la información del usuario, incluido el plan de días al que está suscrito (1-6).
- **Control de Acceso con Tarjeta y Documento:** Se verifica la tarjeta RFID o el documento del usuario para permitir o denegar el acceso.
- **Abono de Cuotas por Meses:** Permite abonar cuotas por 1, 6 o 12 meses para extender la fecha de expiración del plan.
- **Exportar a Excel:** Guarda los datos de los usuarios en un archivo Excel (datos_clientes.xlsx).
- **Control de Acceso según Plan:** Verificación de Ingreso Semanal: Limita el acceso si el usuario ha excedido la cantidad permitida de entradas en la semana, según su plan.

## Notas Importantes

- Asegurarse de tener todos los requisitos instalados antes de ejecutar el programa.
- Configurar el puerto serial en el código Arduino para que coincida con el utilizado en el programa principal (arduino_port = 'COM3').
- La base de datos SQLite se creará automáticamente si no existe.
- La aplicación registra eventos y mensajes en la consola para facilitar la depuración.

¡Disfruta del sistema de control de acceso para tu gimnasio!
