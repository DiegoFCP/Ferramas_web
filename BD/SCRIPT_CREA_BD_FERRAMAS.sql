-- Crear Base de Datos
-- CREATE DATABASE ferramas;

-- CONEXION A BD
-- USE Ferramas;

/*
-- CREACION DE TABLAS

-- Crear tabla de categorías
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Crear tabla de productos
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) CHECK (precio > 0),
    stock INT NOT NULL CHECK (stock >= 0),
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

-- Crear tabla de clientes
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    direccion VARCHAR(200)
);

-- Crear tabla de órdenes
CREATE TABLE ordenes (
    id_orden INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    fecha DATE NOT NULL,
    total DECIMAL(10, 2),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Crear tabla de detalles de órdenes
CREATE TABLE detalles_orden (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_orden INT,
    id_producto INT,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) CHECK (precio_unitario > 0),
    FOREIGN KEY (id_orden) REFERENCES ordenes(id_orden) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Crear tabla de proveedores
CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    correo VARCHAR(100)
);

CREATE TABLE despachos (
    id_despacho INT AUTO_INCREMENT PRIMARY KEY,
    id_orden INT,
    direccion_entrega VARCHAR(200),
    fecha_despacho DATE,
    estado VARCHAR(50),
    FOREIGN KEY (id_orden) REFERENCES ordenes(id_orden) ON DELETE CASCADE
);


ALTER TABLE productos
ADD id_proveedor INT,
ADD FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor);


*/



/*
-- SEEDERS/POBLAR TABLAS


-- Poblar la tabla de categorías
INSERT INTO categorias (nombre, descripcion) VALUES
('Herramientas Eléctricas', 'Categoría para herramientas que funcionan con electricidad');
('Materiales de Construcción', 'Materiales básicos para proyectos de construcción'),
('Pinturas y Acabados', 'Productos para pintar y decorar superficies');

-- Poblar la tabla de productos
INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria) VALUES
('Taladro Makita', 'Taladro Makita', 69990.00, 70, 1);
('Cemento 25kg', 'Bolsa de cemento para construcción', 7500.00, 200, 2),
('Pintura Blanca', 'Pintura lavable para interiores', 12500.00, 150, 3);

-- Poblar la tabla de clientes
INSERT INTO clientes (nombre, correo, direccion) VALUES
('Juan Pérez', 'juanperez@example.com', 'Calle Principal 123'),
('María López', 'marialopez@example.com', 'Avenida Central 456'),
('Diego Cortes', 'diegocortes@example.com', 'Huachimingo 380'),
('Daniel Elgueta', 'danielelgueta@example.com', 'Avenida Peru 666'),
('Sebastian La Rosa', 'sebalarosa@example.com', 'Calle Falsa 123');

-- Poblar la tabla de proveedores
INSERT INTO proveedores (nombre, direccion, correo) VALUES
('Proveedor Bosch', 'Calle de Proveedores 123', 'proveedorbosch@example.com'),
('Materiales de Construcción Ltda', 'Avenida de la Construcción 789', 'materialesltda@example.com');

-- Poblar la tabla de órdenes
INSERT INTO ordenes (id_cliente, fecha, total) VALUES
(1, '2024-10-18', 100490.00),
(2, '2024-10-19', 137500.00);

-- Poblar la tabla de detalles de las órdenes
INSERT INTO detalles_orden (id_orden, id_producto, cantidad, precio_unitario) VALUES
(1, 1, 1, 89990.00),
(1, 2, 1, 7500.00),
(2, 2, 5, 7500.00),
(2, 3, 2, 12500.00);
*/

-- CONSULTAS

SELECT * FROM productos;
SELECT * FROM clientes;
SELECT * FROM ordenes;


-- Consultar todos los productos con su categoría:
SELECT p.nombre AS producto, p.precio, p.stock, c.nombre AS categoria
FROM productos p
JOIN categorias c ON p.id_categoria = c.id_categoria;

-- Órdenes realizadas por un cliente específico:
SELECT o.id_orden, o.fecha, o.total 
FROM ordenes o
JOIN clientes c ON o.id_cliente = c.id_cliente
WHERE c.nombre = 'Juan Pérez';

-- Total de ventas por cliente:
SELECT c.nombre AS cliente, SUM(o.total) AS total_gastado
FROM ordenes o
JOIN clientes c ON o.id_cliente = c.id_cliente
GROUP BY c.nombre;

