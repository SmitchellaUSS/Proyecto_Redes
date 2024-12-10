import socket
import threading
import logging
import psycopg2
import json
from datetime import datetime


logging.basicConfig(filename='system_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname="red_datos",
            user="pokemon",
            password="1234",
            host="localhost"
        )
        return conn
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos: {e}")
        return None


def almacenar_datos_data2(id_device, acc, gyr):
    conn = conectar_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO data_2 (id_device, racc_x, racc_y, racc_z, rgyr_x, rgyr_y, rgyr_z, time_client)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_device, acc['x'], acc['y'], acc['z'], gyr['x'], gyr['y'], gyr['z'], datetime.now()))
                conn.commit()
                logging.info(f"Datos almacenados: Device {id_device}, Acc: {acc}, Gyr: {gyr}")
        except Exception as e:
            logging.error(f"Error al almacenar datos: {e}")
        finally:
            conn.close()


def validar_datos(parsed):
    if not all(key in parsed for key in ['id_device', 'acc', 'gyr']):
        raise ValueError("Estructura de datos inválida")
    acc = parsed['acc']
    gyr = parsed['gyr']
    if not (all(k in acc for k in ['x', 'y', 'z']) and all(k in gyr for k in ['x', 'y', 'z'])):
        raise ValueError("Datos de acc o gyr incompletos")
    return parsed['id_device'], acc, gyr


def manejar_tcp(cliente, direccion):
    logging.info(f"Conexión TCP desde {direccion}")
    error_count = 0
    while True:
        try:
            datos = cliente.recv(1024).decode()
            if not datos:
                break
            parsed = json.loads(datos)  # Procesar como JSON
            id_device, acc, gyr = validar_datos(parsed)
            almacenar_datos_data2(id_device, acc, gyr)
            cliente.sendall("Datos recibidos".encode())
            error_count = 0  # Reinicia el contador de errores
        except json.JSONDecodeError:
            logging.error(f"Datos malformados desde {direccion}")
            cliente.sendall("Error: datos malformados".encode())
            error_count += 1
        except ValueError as e:
            logging.error(f"Validación fallida desde {direccion}: {e}")
            cliente.sendall(f"Error: {e}".encode())
            error_count += 1
        except Exception as e:
            logging.error(f"Error inesperado desde {direccion}: {e}")
            cliente.sendall("Error: problema interno del servidor".encode())
            error_count += 1
        if error_count >= 3:  # Desconectar tras 3 errores consecutivos
            logging.warning(f"Conexión cerrada debido a múltiples errores desde {direccion}")
            break
    cliente.close()


def manejar_udp(servidor):
    while True:
        try:
            datos, direccion = servidor.recvfrom(1024)
            datos = datos.decode()
            parsed = json.loads(datos)  # Procesar como JSON
            id_device, acc, gyr = validar_datos(parsed)
            almacenar_datos_data2(id_device, acc, gyr)
        except json.JSONDecodeError:
            logging.error(f"Datos malformados desde {direccion}")
        except ValueError as e:
            logging.error(f"Validación fallida desde {direccion}: {e}")
        except Exception as e:
            logging.error(f"Error inesperado desde {direccion}: {e}")


if __name__ == "__main__":
    tcp_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_servidor.bind(("0.0.0.0", 5000))
    tcp_servidor.listen(5)

    udp_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_servidor.bind(("0.0.0.0", 5001))

    threading.Thread(target=lambda: manejar_udp(udp_servidor), daemon=True).start()
    logging.info("Servidor UDP en el puerto 5001 iniciado")
    logging.info("Servidor TCP en el puerto 5000 iniciado")

    while True:
        cliente, direccion = tcp_servidor.accept()
        threading.Thread(target=manejar_tcp, args=(cliente, direccion), daemon=True).start()
