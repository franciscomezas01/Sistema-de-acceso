import serial
import time

# Abre el puerto serial (asegúrate de que coincida con el puerto que está usando Arduino)
arduino_port = 'COM3'
ser = serial.Serial(arduino_port, 9600, timeout=1)

try:
    while True:
        # Lee la línea recibida desde Arduino
        line = ser.readline().decode('utf-8').rstrip()
        
        if line:
            print("id de tarjeta", line)

        time.sleep(1)

except KeyboardInterrupt:
    ser.close()
    print("Conexión cerrada.")
