-- =====================================================================
-- Sistema de Gestión de Consultas Médicas
-- Script de creación de base de datos (DDL) + datos de prueba
-- Motor: MySQL 8.0
-- Autor: Braulio Yael Carranza Zamora
-- Materia: Ingeniería de Software
-- =====================================================================

DROP DATABASE IF EXISTS consultas_medicas;
CREATE DATABASE consultas_medicas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE consultas_medicas;

-- =====================================================================
-- Tabla: usuarios
-- Propósito: Autenticación y control de acceso por roles
-- =====================================================================
CREATE TABLE usuarios (
    id_usuario   INT AUTO_INCREMENT PRIMARY KEY,
    usuario      VARCHAR(50)  NOT NULL UNIQUE,
    password     VARCHAR(255) NOT NULL,
    nombre       VARCHAR(100) NOT NULL,
    rol          ENUM('Administrador','Recepcionista') NOT NULL,
    activo       TINYINT(1) NOT NULL DEFAULT 1,
    fecha_alta   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================================
-- Tabla: pacientes
-- =====================================================================
CREATE TABLE pacientes (
    id_paciente  INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    apellidos    VARCHAR(100) NOT NULL,
    fecha_nac    DATE NOT NULL,
    sexo         ENUM('M','F','O') NOT NULL,
    telefono     VARCHAR(15),
    email        VARCHAR(100) UNIQUE,
    direccion    VARCHAR(200),
    fecha_alta   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================================
-- Tabla: medicos
-- =====================================================================
CREATE TABLE medicos (
    id_medico    INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    apellidos    VARCHAR(100) NOT NULL,
    especialidad VARCHAR(80)  NOT NULL,
    cedula       VARCHAR(20)  NOT NULL UNIQUE,
    telefono     VARCHAR(15),
    email        VARCHAR(100) UNIQUE,
    activo       TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB;

-- =====================================================================
-- Tabla: citas
-- =====================================================================
CREATE TABLE citas (
    id_cita      INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora   DATETIME NOT NULL,
    estado       ENUM('Pendiente','Confirmada','Atendida','Cancelada')
                     NOT NULL DEFAULT 'Pendiente',
    motivo       VARCHAR(255),
    id_paciente  INT NOT NULL,
    id_medico    INT NOT NULL,
    fecha_alta   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_citas_paciente
        FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_citas_medico
        FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_citas_fecha   ON citas(fecha_hora);
CREATE INDEX idx_citas_paciente ON citas(id_paciente);
CREATE INDEX idx_citas_medico  ON citas(id_medico);

-- =====================================================================
-- Tabla: expedientes
-- Un expediente se genera tras atender una cita (1:1)
-- =====================================================================
CREATE TABLE expedientes (
    id_expediente INT AUTO_INCREMENT PRIMARY KEY,
    id_cita       INT NOT NULL UNIQUE,
    diagnostico   TEXT NOT NULL,
    tratamiento   TEXT,
    observaciones TEXT,
    fecha_alta    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_expediente_cita
        FOREIGN KEY (id_cita) REFERENCES citas(id_cita)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =====================================================================
-- Datos de prueba (seed)
-- Contraseñas hasheadas con SHA-256
--   admin    -> admin123
--   recep    -> recep123
-- =====================================================================
INSERT INTO usuarios (usuario, password, nombre, rol) VALUES
 ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
  'Braulio Yael Carranza Zamora', 'Administrador'),
 ('recep', 'b59e29d85d39d5cc5f50b8bdf85bbcdb35a3128b6f5de1d4c02c8cb61f2d3dc8',
  'Ana López Hernández', 'Recepcionista');

INSERT INTO medicos (nombre, apellidos, especialidad, cedula, telefono, email) VALUES
 ('Roberto', 'Ruiz Martínez',  'Cardiología',     'CED-1001', '3312345001', 'rruiz@clinicasalud.mx'),
 ('Verónica','Vega Castillo',   'Neurología',      'CED-1002', '3312345002', 'vvega@clinicasalud.mx'),
 ('Fernando','Pérez Galindo',   'Medicina General','CED-1003', '3312345003', 'fperez@clinicasalud.mx'),
 ('Lucía',   'Mendoza Ruvalcaba','Pediatría',      'CED-1004', '3312345004', 'lmendoza@clinicasalud.mx');

INSERT INTO pacientes (nombre, apellidos, fecha_nac, sexo, telefono, email, direccion) VALUES
 ('Juan',    'López Ramírez',   '1985-03-14', 'M', '3311112201', 'jlopez@correo.com',  'Av. Vallarta 1500, Guadalajara'),
 ('María',   'García Sánchez',  '1992-07-22', 'F', '3311112202', 'mgarcia@correo.com', 'C. Hidalgo 230, Zapopan'),
 ('Carlos',  'Hernández Soto',  '1978-11-05', 'M', '3311112203', 'chernandez@correo.com','Av. Patria 400, Tlaquepaque'),
 ('Sofía',   'Ramírez Núñez',   '2001-01-30', 'F', '3311112204', 'sramirez@correo.com','C. Juárez 88, Tonalá'),
 ('Diego',   'Torres Vázquez',  '1995-09-18', 'M', '3311112205', 'dtorres@correo.com', 'Av. México 1200, Guadalajara');

INSERT INTO citas (fecha_hora, estado, motivo, id_paciente, id_medico) VALUES
 ('2026-04-10 09:00:00', 'Atendida',   'Dolor en el pecho',          1, 1),
 ('2026-04-12 11:30:00', 'Atendida',   'Migrañas recurrentes',       2, 2),
 ('2026-04-15 16:00:00', 'Confirmada', 'Chequeo general',            3, 3),
 ('2026-04-20 10:00:00', 'Pendiente',  'Vacunación pediátrica',      4, 4),
 ('2026-04-28 13:30:00', 'Cancelada',  'Reagendar',                  5, 3),
 ('2026-04-30 09:30:00', 'Pendiente',  'Seguimiento cardiológico',   1, 1);

INSERT INTO expedientes (id_cita, diagnostico, tratamiento, observaciones) VALUES
 (1, 'Hipertensión arterial leve', 'Losartán 50mg cada 24h por 30 días', 'Reducir consumo de sal y caminar 30 min diarios.'),
 (2, 'Migraña con aura',           'Sumatriptán 50mg PRN', 'Llevar diario de cefaleas durante 4 semanas.');

-- =====================================================================
-- Vistas útiles para reportes
-- =====================================================================
CREATE OR REPLACE VIEW v_citas_detalle AS
SELECT  c.id_cita,
        c.fecha_hora,
        c.estado,
        c.motivo,
        CONCAT(p.nombre,' ',p.apellidos) AS paciente,
        CONCAT(m.nombre,' ',m.apellidos) AS medico,
        m.especialidad
FROM    citas c
JOIN    pacientes p ON p.id_paciente = c.id_paciente
JOIN    medicos   m ON m.id_medico   = c.id_medico;

CREATE OR REPLACE VIEW v_expedientes_detalle AS
SELECT  e.id_expediente,
        e.fecha_alta,
        e.diagnostico,
        e.tratamiento,
        CONCAT(p.nombre,' ',p.apellidos) AS paciente,
        CONCAT(m.nombre,' ',m.apellidos) AS medico,
        m.especialidad,
        c.fecha_hora AS fecha_cita
FROM    expedientes e
JOIN    citas c     ON c.id_cita     = e.id_cita
JOIN    pacientes p ON p.id_paciente = c.id_paciente
JOIN    medicos   m ON m.id_medico   = c.id_medico;

-- Fin del script.
