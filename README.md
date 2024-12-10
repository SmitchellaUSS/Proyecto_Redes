# Proyecto con Docker y Docker Compose

## Instrucciones

1. Clona el repositorio:
   ```bash
   git clone https://github.com/SmitchellaUSS/Proyecto_Redes.git
   cd Proyecto_Redes

2.Construye y ejecuta los contenedores:
   ```bash
   docker-compose up --build

Los servicios estarán disponibles en:
CP: localhost:5000
UDP: localhost:5001
Base de datos: localhost:5432

### Notas
1. **Archivos Python:** Solo es necesario ejecutar `server.py` como el servicio principal.
2.Configura el punto de acceso Wi-Fi: El script incluido configura automáticamente hostapd y dnsmasq para crear un punto de acceso Wi-Fi.


