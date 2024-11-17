CREATE DATABASE Greenplum

USE Greenplum

CREATE TABLE customers (
    customer_id INT PRIMARY KEY IDENTITY(1,1),  -- Auto-incrementing ID
    customer_name NVARCHAR(255) NOT NULL,        
    email_address NVARCHAR(255) UNIQUE NOT NULL,  -- Email should be unique for each customer
    country NVARCHAR(100) NOT NULL              
);

CREATE TABLE products (
    product_id INT PRIMARY KEY IDENTITY(1,1),  -- Auto-incrementing ID for products
    product_name NVARCHAR(255) NOT NULL,       
    price DECIMAL(10, 2) NOT NULL,             -- Price of the product with 2 decimal precision
    category NVARCHAR(100) NOT NULL             
);

CREATE TABLE sales_transactions (
    transaction_id INT PRIMARY KEY IDENTITY(1,1),  -- Auto-incrementing transaction ID
    customer_id INT NOT NULL,                       
    product_id INT NOT NULL,                        
    purchase_date DATETIME NOT NULL DEFAULT GETDATE(), -- Date of the purchase
    quantity INT NOT NULL,                          
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),  -- FK to customers table
    FOREIGN KEY (product_id) REFERENCES products(product_id)     -- FK to products table
);


CREATE TABLE shipping_details (
    transaction_id INT PRIMARY KEY,                -- Primary and Foreign key referencing sales_transactions table
    shipping_date DATETIME NOT NULL,               
    shipping_address NVARCHAR(255) NOT NULL,       
    city NVARCHAR(100) NOT NULL,                   
    country NVARCHAR(100) NOT NULL,                
    FOREIGN KEY (transaction_id) REFERENCES sales_transactions(transaction_id)  -- FK to sales_transactions table
);


-- create index on purchase_date column to analyze data more quickly.
CREATE INDEX idx_purchase_date ON sales_transactions (purchase_date);

