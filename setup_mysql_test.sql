-- MySQL setup test

-- creating database hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- creating user hbnb_test
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- granting all privileges to user
USE hbnb_test_db;
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- granting select privilege on performance_schema
USE performance_schema;
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- flush privileges
FLUSH PRIVILEGES;
