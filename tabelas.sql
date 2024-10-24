CREATE TABLE autores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE, 
    pais_origem VARCHAR(100) NOT NULL  
);

CREATE TABLE editoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE, 
    cidade VARCHAR(100) NOT NULL  
);

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE 
);

CREATE TABLE gibis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,  
    ano INT NOT NULL,  
    editora_id INT NOT NULL,  
    autor_id INT NOT NULL,  
    categoria_id INT NOT NULL,  
    FOREIGN KEY (editora_id) REFERENCES editoras(id),
    FOREIGN KEY (autor_id) REFERENCES autores(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);
