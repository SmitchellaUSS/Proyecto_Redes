import socket
import json
import time

# Configuración de envío
SERVER_IP = "172.17.0.1"  # Cambia a la IP del servidor Raspberry Pi
TCP_PORT = 5000
UDP_PORT = 5001

# Ejemplo de datos JSON
data = {
    "id_device": 1,
    "acc": {
        "x": 1.2,
        "y": -0.5,
        "z": 9.8
    },
    "gyr": {
        "x": 50.0,
        "y": -20.0,
        "z": 0.0
    }
}

# Función para enviar datos por TCP
def enviar_tcp():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((SERVER_IP, TCP_PORT))
            json_data = json.dumps(data)
            tcp_socket.sendall(json_data.encode())
            response = tcp_socket.recv(1024).decode()
            print(f"Respuesta del servidor: {response}")
    except Exception as e:
        print(f"Error enviando por TCP: {e}")

# Función para enviar datos por UDP
def enviar_udp():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            json_data = json.dumps(data)
            udp_socket.sendto(json_data.encode(), (SERVER_IP, UDP_PORT))
            print("Datos enviados por UDP.")
    except Exception as e:
        print(f"Error enviando por UDP: {e}")

# Enviar datos por ambos métodos
if __name__ == "__main__":
    while True:
        print("Enviando datos por TCP...")
        enviar_tcp()
        print("Enviando datos por UDP...")
        enviar_udp()
        time.sleep(5)  # Envía cada 5 segundos
