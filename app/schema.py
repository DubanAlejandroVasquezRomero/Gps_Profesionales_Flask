instructions = [
"""
CREATE TABLE profesional (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100) NOT NULL,
    especializacion VARCHAR(100),
    comuna VARCHAR(100) 
);
""",

"""
CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);
""",

"""
CREATE TABLE servicios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria_id INT,
    profesional_id BIGINT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (profesional_id) REFERENCES profesional(id)
);
""",

"""

CREATE TABLE ubicacion (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6),
    profesional_id BIGINT,
    FOREIGN KEY (profesional_id) REFERENCES profesional(id)
);

""",

"""
CREATE TABLE horarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profesional_id BIGINT,
    dia VARCHAR(100),
    hora_inicio TIME,
    hora_fin TIME,
    FOREIGN KEY (profesional_id) REFERENCES profesional(id)
);
""",

"""
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario VARCHAR(50) NOT NULL, 
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    contraseña VARCHAR(200) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    profesional_id BIGINT,
    FOREIGN KEY (profesional_id) REFERENCES profesional(id)
);
"""
]
