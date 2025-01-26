CREATE DATABASE agroforestry_app;

USE agroforestry_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('field_executive', 'field_manager', 'senior_manager') NOT NULL
);

CREATE TABLE farmers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    plot_location VARCHAR(255) NOT NULL,
    added_by VARCHAR(50) NOT NULL
);

CREATE TABLE tree_species (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    species_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE CASCADE
);

INSERT INTO users (username, password, role)
VALUES
('executive_a', 'password_a', 'field_executive'),
('executive_b', 'password_b', 'field_executive'),
('manager_c', 'password_c', 'field_manager'),
('manager_d', 'password_d', 'field_manager'),
('senior_manager', 'password_e', 'senior_manager');

ALTER TABLE farmers ADD COLUMN field_photo_blob LONGBLOB;

ALTER TABLE farmers DROP COLUMN field_photo;
