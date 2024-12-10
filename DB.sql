-- Crear la base de datos
CREATE DATABASE red_datos;

-- Conectar a la base de datos creada (en el cliente de PostgreSQL)
\c red_datos;

-- Crear la tabla "Log"
CREATE TABLE Log (
    Id_device INT NOT NULL,
    Status_report INT,
    Time_server TIMESTAMP,
    PRIMARY KEY (Id_device)
);

-- Crear la tabla "Data_2"
CREATE TABLE Data_2 (
    Id_device INT NOT NULL,
    Racc_x FLOAT,
    Racc_y FLOAT,
    Racc_z FLOAT,
    Rgyr_x FLOAT,
    Rgyr_y FLOAT,
    Rgyr_z FLOAT,
    Time_client TIMESTAMP,
    PRIMARY KEY (Id_device)
);

-- Crear la tabla "configuration"
CREATE TABLE configuration (
    Id_device INT NOT NULL,
    TCP_PORT INT,
    UDP_port INT,
    Host_ip_addr INT,
    Ssid VARCHAR(45),
    Pass VARCHAR(45),
    PRIMARY KEY (Id_device)
);
