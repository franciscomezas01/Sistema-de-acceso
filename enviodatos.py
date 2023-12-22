import serial
import time

# Configuración del puerto serial
puerto_serial = "COM3"
baud_rate = 9600

# Inicializar el puerto serial
ser = serial.Serial(puerto_serial, baud_rate, timeout=1)


    # Enviar el número 1 al Arduino
for range in (1,2):
    ser.write(b'0')
    time.sleep(2)
    

