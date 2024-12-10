import socket
import json
import time

def enviar_mensaje_tcp(host, puerto, mensaje):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((host, puerto))
            cliente.sendall(mensaje.encode())
            respuesta = cliente.recv(1024).decode()
            print(f"Respuesta del servidor: {respuesta}")
    except Exception as e:
        print(f"Error al enviar mensaje TCP: {e}")

def enviar_mensaje_udp(host, puerto, mensaje):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
            cliente.sendto(mensaje.encode(), (host, puerto))
    except Exception as e:
        print(f"Error al enviar mensaje UDP: {e}")

if __name__ == "__main__":
    host = "192.168.4.84"  # Dirección IP del servidor
    puerto_tcp = 5000   # Puerto TCP del servidor
    puerto_udp = 5001   # Puerto UDP del servidor

    # Mensajes para probar el servidor
    mensajes_corruptos = [
        "mensaje no válido",                     # Texto plano
        "{id_device: 123, acc: {x: 0}}",        # JSON malformado (comillas faltantes)
        '{"id_device": "abc", "acc": {}}',      # Claves vacías en el JSON
        '{"id_device": 123}',                   # Falta 'acc' y 'gyr'
        '{"id_device": 123, "acc": null}',      # 'acc' es nulo
        '{"id_device": 123, "acc": {}, "gyr": {}}', # 'acc' y 'gyr' incompletos
    ]

    print("Enviando mensajes TCP...")
    for mensaje in mensajes_corruptos:
        print(f"Enviando mensaje: {mensaje}")
        enviar_mensaje_tcp(host, puerto_tcp, mensaje)
        time.sleep(1)  # Esperar un segundo entre mensajes

    print("\nEnviando mensajes UDP...")
    for mensaje in mensajes_corruptos:
        print(f"Enviando mensaje: {mensaje}")
        enviar_mensaje_udp(host, puerto_udp, mensaje)
        time.sleep(1)  # Esperar un segundo entre mensajes
