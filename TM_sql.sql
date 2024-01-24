CREATE DATABASE task_manager_db;

CREATE USER 'task_manager_user'@'localhost' IDENTIFIED BY 'TM123';

GRANT ALL PRIVILEGES ON task_manager_db.* TO 'task_manager_user'@'localhost';

FLUSH PRIVILEGES;


