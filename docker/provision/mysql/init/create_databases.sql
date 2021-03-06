CREATE DATABASE trader_dev;
CREATE DATABASE trader_test; 

\c trader_dev;
CREATE TABLE IF NOT EXISTS users (
     email VARCHAR(255) UNIQUE NOT NULL,
     username VARCHAR(255) NOT NULL,
     password VARCHAR(255) NOT NULL,
     id SERIAL PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS investments (
     stock_name VARCHAR(255) NOT NULL,
     usd_value NUMERIC NOT NULL,
     bitcoin_value NUMERIC,
     is_bitcoin BOOLEAN NOT NULL,
     id SERIAL PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS user_investments (
     user_id INTEGER NOT NULL REFERENCES users(id),
     investment_id INTEGER NOT NULL REFERENCES investments(id),
     usd_value NUMERIC NOT NULL,
     id SERIAL PRIMARY KEY NOT NULL
);

\c trader_test;
CREATE TABLE IF NOT EXISTS users (
     email VARCHAR(255) UNIQUE NOT NULL,
     username VARCHAR(255) NOT NULL,
     password VARCHAR(255) NOT NULL,
     id SERIAL PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS investments (
     stock_name VARCHAR(255) NOT NULL,
     usd_value NUMERIC NOT NULL,
     bitcoin_value NUMERIC,
     is_bitcoin BOOLEAN NOT NULL,
     id SERIAL PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS user_investments (
     user_id INTEGER NOT NULL REFERENCES users(id),
     investment_id INTEGER NOT NULL REFERENCES investments(id),
     usd_value NUMERIC NOT NULL,
     id SERIAL PRIMARY KEY NOT NULL
);
