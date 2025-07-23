-- Base de datos para el sistema del asadero

-- Tabla de productos
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(255) NOT NULL,
    stock INT NOT NULL
);

-- Tabla de clientes
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20)
);

-- Tabla de pedidos
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Tabla de detalles de pedido
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Tabla de compras
CREATE TABLE purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_date DATETIME NOT NULL,
    supplier VARCHAR(255),
    total_amount DECIMAL(10, 2) NOT NULL
);

-- Tabla de detalles de compra
CREATE TABLE purchase_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES purchases(id)
);

-- Insertar algunas categorías de productos iniciales
INSERT INTO products (name, description, price, category, stock) VALUES
('Almuerzo Ejecutivo', 'Plato del día con sopa, segundo y bebida', 5.00, 'Almuerzos', 50),
('Coca-Cola', '500ml', 1.00, 'Gaseosas', 100),
('Conejo Asado', 'Conejo entero asado a la parrilla', 15.00, 'Conejos Asados', 20),
('Cuy Asado', 'Cuy entero asado a la parrilla', 20.00, 'Cuyes Asados', 15),
('Parrillada para 2', 'Churrasco, chorizo, pollo y papas', 25.00, 'Parrilladas', 30);
