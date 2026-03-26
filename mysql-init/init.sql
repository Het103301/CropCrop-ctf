CREATE DATABASE IF NOT EXISTS corp_portal;
USE corp_portal;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(32) DEFAULT 'employee',
    email VARCHAR(128),
    department VARCHAR(64)
);

CREATE TABLE employee_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    salary DECIMAL(10,2),
    ssn VARCHAR(16),
    notes TEXT,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (username, password, role, email, department) VALUES
('admin', 'sup3rs3cr3t!', 'admin', 'admin@corpcorp.internal', 'IT'),
('jsmith', 'password123', 'employee', 'jsmith@corpcorp.internal', 'Finance'),
('mwilson', 'qwerty99', 'employee', 'mwilson@corpcorp.internal', 'HR'),
('tgraves', 'letmein', 'manager', 'tgraves@corpcorp.internal', 'Operations');

INSERT INTO employee_records (user_id, salary, ssn, notes, message) VALUES
(1, 120000.00, '000-00-0001', 'Full system access', 'Nothing to see here.'),
(2, 75000.00, '123-45-6789', 'Quarterly review pending', 'FLAG{cr0pcr0p_sql1_d4t4_3xf1l_success}'),
(3, 68000.00, '987-65-4321', 'PTO balance: 12 days', 'See you at the team lunch Friday!'),
(4, 95000.00, '555-12-3456', 'Manager of Q3 project', 'Reminder: submit timesheets by EOD.');
