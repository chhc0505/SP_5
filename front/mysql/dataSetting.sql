CREATE DATABASE user_db;
USE user_db;
CREATE TABLE user (
    user_id VARCHAR(50) NOT NULL PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL,
    user_password VARCHAR(50) NOT NULL
);

CREATE DATABASE ranking_db;
USE ranking_db;
CREATE TABLE ranking (
    user_id VARCHAR(50) NOT NULL PRIMARY KEY,
    score int DEFAULT 0
);