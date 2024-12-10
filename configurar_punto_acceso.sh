#!/bin/bash

echo "Configurando hostapd..."
cat <<EOL > /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=WifiRaspBerry
hw_mode=g
channel=6
auth_algs=1
wpa=2
wpa_passphrase=porygonz
EOL

echo "Configurando dnsmasq..."
cat <<EOL > /etc/dnsmasq.conf
interface=wlan0
dhcp-range=192.168.50.10,192.168.50.100,24h
EOL

echo "Habilitando el reenvío de tráfico..."
# Asegúrate de que el contenedor tenga permisos para modificar este valor
echo "net.ipv4.ip_forward=1" >> /proc/sys/net/ipv4/ip_forward

echo "Reiniciando servicios..."
# Usa los servicios directamente sin `sudo`
systemctl restart hostapd || echo "Error al reiniciar hostapd. ¿Está instalado?"
systemctl restart dnsmasq || echo "Error al reiniciar dnsmasq. ¿Está instalado?"

echo "Configuración completada."
"
