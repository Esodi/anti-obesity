-- Creating the database
CREATE DATABASE IF NOT EXISTS webappdb;

-- Creating the user with the specified password
CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'user';

-- Granting all privileges on the database to the user
GRANT ALL PRIVILEGES ON webappdb.* TO 'user'@'localhost';

-- Flushing privileges to ensure that all changes take effect
FLUSH PRIVILEGES;
