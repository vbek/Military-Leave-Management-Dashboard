CREATE DATABASE IF NOT EXISTS bibekdb;
CREATE USER IF NOT EXISTS 'appuser'@'localhost' IDENTIFIED BY 'unit123';
GRANT ALL ON bibekdb.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;