CREATE DATABASE trader_dev;
CREATE DATABASE trader_test; 

\c trader_dev;
CREATE TABLE IF NOT EXISTS users (
     email VARCHAR(255) UNIQUE NOT NULL,
     username VARCHAR(255) NOT NULL,
     password VARCHAR(255) NOT NULL,
     id SERIAL PRIMARY KEY NOT NULL
);

\c trader_test;
CREATE TABLE IF NOT EXISTS users (
     email VARCHAR(255) UNIQUE NOT NULL,
     username VARCHAR(255) NOT NULL,
     password VARCHAR(255) NOT NULL,
     id SERIAL PRIMARY KEY NOT NULL
);