CREATE DATABASE IF NOT EXISTS educaplan;

CREATE USER IF NOT EXISTS 'superuser'@'%' IDENTIFIED BY 'superuser';
GRANT ALL PRIVILEGES ON python_project.* TO 'superuser'@'%';
FLUSH PRIVILEGES;

USE educaplan;