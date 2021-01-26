CREATE DATABASE sports_analytics_proj;
USE sports_analytics_proj;
CREATE TABLE user (
    id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE KEY,
    email VARCHAR(50) NOT NULL UNIQUE KEY,
    password_hash CHAR(128) NOT NULL
);
