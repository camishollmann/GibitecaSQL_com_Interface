-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 25/10/2024 às 19:44
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

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

INSERT INTO `editoras` (`id`, `nome`, `cidade`) VALUES
(1, 'UFPR', 'Curitiba');

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE 
);

INSERT INTO `categorias` (`id`, `nome`) VALUES
(1, 'Aventura');

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
