CREATE DATABASE IF NOT EXISTS employees;
USE employees;

CREATE TABLE IF NOT EXISTS employee(
emp_id VARCHAR(20),
first_name VARCHAR(20),
last_name VARCHAR(20),
primary_skill VARCHAR(20),
location VARCHAR(20));

INSERT INTO employee 
(emp_id, first_name, last_name, primary_skill, location) VALUES 
('1','Amanda','Williams','Smile','local'),
('2','Maharshi','Mehta','System Engineer','North York'),
('3','Ghufran','Ataie','DB Developer','Ajax'),
('4','Vibha','Thakkar','Marketing Officer','Scarborough')
;
SELECT * FROM employee;