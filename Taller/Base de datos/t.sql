CREATE DATABASE IF NOT EXISTS `Taller_Mecanico`;

USE `Taller_Mecanico`;

CREATE TABLE IF NOT EXISTS `Clientes` (
    `DNI` VARCHAR(50) PRIMARY KEY,
    `Nombre` VARCHAR(50),
    `Apellido` VARCHAR(50),
    `Direccion` VARCHAR(50),
    `Telefono` VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS `Vehiculos` (
    `Patente` VARCHAR(50) PRIMARY KEY,
    `DNI` VARCHAR(50),
    `Marca` VARCHAR(50),
    `Modelo` VARCHAR(50),
    `Color` VARCHAR(50),
    FOREIGN KEY (`DNI`) REFERENCES `Clientes`(`DNI`)
);

CREATE TABLE IF NOT EXISTS `Mecanicos` (
    `Legajo` VARCHAR(50) PRIMARY KEY,
    `Nombre` VARCHAR(50),
    `Apellido` VARCHAR(50),
    `Rol` VARCHAR(50),
    `Estado` VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS `Reparaciones` (
    `ID` VARCHAR(50) PRIMARY KEY,
    `Patente` VARCHAR(50),
    `DNI` VARCHAR(50),
    `Legajo` VARCHAR(50),
    `Fecha` DATE,
    FOREIGN KEY (`Patente`) REFERENCES `Vehiculos`(`Patente`),
    FOREIGN KEY (`DNI`) REFERENCES `Clientes`(`DNI`),
    FOREIGN KEY (`Legajo`) REFERENCES `Mecanicos`(`legajo`)
);

CREATE TABLE IF NOT EXISTS `Repuestos_Reparacion` (
	`Codigo_repuesto` VARCHAR(50) PRIMARY KEY,
    `Precio` FLOAT,
    `Cant_rep` int,
    `Importe` FLOAT GENERATED ALWAYS AS ( `Precio` *  `Cant_rep`) STORED,
    `Descripcion` VARCHAR(50)
);

create table if not exists `Proveedores`(
	`Cod_prov` varchar(50) primary key,
    `Nombre` varchar(50),
    `Telefono` varchar(50),
    `Email` varchar(50),
    `Direccion` varchar(50)
);

CREATE TABLE IF NOT EXISTS  `Stock`(
	`Codigo_repuesto` VARCHAR(50) PRIMARY KEY,
    `Descripcion` VARCHAR(50),
    `Cant_rep_libre` int,
    `Cant_rep_total` int,
    `Proveedor` varchar(50),
    FOREIGN KEY (`Proveedor`) REFERENCES `Proveedores`(`Cod_prov`),
    `Precio` FLOAT
);

CREATE TABLE IF NOT EXISTS `Usuarios` (
    `Usuario` VARCHAR(50) PRIMARY KEY,
    `Clave` VARCHAR(50),
    `Nombre` VARCHAR(50),
    `Apellido` VARCHAR(50)
);


