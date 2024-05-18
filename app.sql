-- Create and use the Company database
CREATE DATABASE IF NOT EXISTS Company;
USE Company;

-- Drop existing tables to avoid conflicts
DROP TABLE IF EXISTS Works_On;
DROP TABLE IF EXISTS Project;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Team;

-- Create Department table
CREATE TABLE Department (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

-- Insert data into Department table
INSERT INTO Department (dept_id, dept_name) VALUES
(1, 'HR'),
(2, 'Engineering'),
(3, 'Sales');

-- Create Employee table
CREATE TABLE Employee (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_name VARCHAR(255) NOT NULL,
    dob DATE,
    contact VARCHAR(15),
    email VARCHAR(255),
    address TEXT,
    dept_id INT,
    supervisor_id INT,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id),
    FOREIGN KEY (supervisor_id) REFERENCES Employee(emp_id)
);

-- Insert data into Employee table
INSERT INTO Employee (emp_name, dob, contact, email, address, dept_id, supervisor_id) VALUES
('Alice', '1990-05-14', '555-1234', 'alice@example.com', '123 Elm St', 1, NULL), -- Alice doesn't have a supervisor
('Bob', '1985-03-22', '555-5678', 'bob@example.com', '456 Oak St', 2, 1), -- Bob's supervisor is Alice
('Charlie', '1979-11-10', '555-8765', 'charlie@example.com', '789 Pine St', 2, 1), -- Charlie's supervisor is also Alice
('David', '1992-07-30', '555-4321', 'david@example.com', '321 Maple St', 3, 1);

-- Create Team table
CREATE TABLE Team (
    team_id INT PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(50) NOT NULL,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
);

-- Insert data into Team table
INSERT INTO Team (team_name, dept_id) VALUES
('Team Alpha', 2),
('Team Beta', 3);

-- Create Project table
CREATE TABLE Project (
    proj_id INT PRIMARY KEY AUTO_INCREMENT,
    proj_name VARCHAR(50) NOT NULL,
    start_date DATE,
    end_date DATE,
    dept_id INT,
    team_head INT,
    budget DECIMAL(10, 2),
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id),
    FOREIGN KEY (team_head) REFERENCES Employee(emp_id)
);

-- Insert data into Project table
INSERT INTO Project (proj_name, start_date, end_date, dept_id, team_head, budget) VALUES
('Project A', '2024-01-01', '2024-12-31', 2, 2, 50000.00),
('Project B', '2024-06-01', '2025-05-31', 3, 3, 75000.00);

-- Create Works_On table
CREATE TABLE Works_On (
    emp_id INT,
    proj_id INT,
    PRIMARY KEY (emp_id, proj_id),
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id),
    FOREIGN KEY (proj_id) REFERENCES Project(proj_id),
    hours_worked INT
);

-- Insert data into Works_On table
INSERT INTO Works_On (emp_id, proj_id, hours_worked) VALUES
(2, 1, 120),
(3, 1, 150),
(4, 2, 100);
