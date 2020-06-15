CREATE DATABASE myflaskapp;

CREATE TABLE users(
  id INT(11) AUTO_INCREMENT primary key,
  name VARCHAR(100),
  email VARCHAR(100),
  username VARCHAR(30),
  password VARCHAR(100),
  register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE articles (
  id INT(11) AUTO_INCREMENT primary KEY,
  title VARCHAR(255),
  author VARCHAR(100),
  body TEXT,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
