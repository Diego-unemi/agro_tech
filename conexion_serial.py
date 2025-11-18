import serial
import requests
import json
import time

SERIAL_PORT = 'COM3'  # Ajusta según tu puerto
BAUD_RATE = 115200
DJANGO_URL = 'http://127.0.0.1:8000/recibir_datos/'

print(f"Escuchando en el puerto {SERIAL_PORT} a {BAUD_RATE} baudios...")
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

while True:
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        
        if line:
            print(f"Dato recibido del ESP32: {line}")
            try:
                data = json.loads(line)
                response = requests.post(DJANGO_URL, json=data)
                print(f"Enviado a Django. Respuesta: {response.status_code} - {response.text}")
                
            except json.JSONDecodeError:
                print("Error: No es un JSON válido")
            except requests.exceptions.RequestException as e:
                print(f"Error al conectar con Django: {e}")
                
    except serial.SerialException as e:
        print(f"Error en el puerto serie: {e}")
        time.sleep(5)
    except KeyboardInterrupt:
        print("Programa detenido")
        break

ser.close()