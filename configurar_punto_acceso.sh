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
sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf

echo "Reiniciando servicios..."
sudo systemctl restart hostapd
sudo systemctl restart dnsmasq

echo "Configuración completada."
