CREATE DATABASE UO300568_DB
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE UO300568_DB;

CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY CHECK (id_usuario BETWEEN 1 AND 12),
    profesion VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    genero ENUM('Hombre', 'Mujer', 'Otro') NOT NULL,
    pericia INT NOT NULL CHECK (pericia BETWEEN 0 AND 10)
);

CREATE TABLE pruebas (
    id_prueba INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    dispositivo ENUM('ordenador','tableta','telefono') NOT NULL,
    tiempo_segundos INT NOT NULL,
    completado BOOLEAN NOT NULL,
    comentarios_usuario TEXT,
    mejoras TEXT,
    valoracion INT CHECK (valoracion BETWEEN 0 AND 10),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE observaciones (
    id_observacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    comentarios TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);