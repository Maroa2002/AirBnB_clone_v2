-- prepares a MySQL server
-- .* denotes all tablesecho "SHOW DATABASES;" | mysql -uhbnb_dev -p | grep hbnb_dev_db

-- creating database hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- creating user hbnb_dev
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- granting user all privileges
USE hbnb_dev_db;
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- granting select privilege
USE performance_schema;
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- flush privileges
FLUSH PRIVILEGES;
