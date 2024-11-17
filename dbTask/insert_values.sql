CREATE PROCEDURE InsertRandomSalesTransactions
AS
BEGIN
    DECLARE @i INT = 1;
    DECLARE @start_date DATE = '2024-07-30'; -- Starting date for transactions

    -- Loop to insert 100 rows
    WHILE @i <= 100
    BEGIN
        INSERT INTO sales_transactions (customer_id, product_id, purchase_date, quantity)
        VALUES 
            (
                -- Random customer_id between 1 and 4
                FLOOR(RAND() * 4) + 1, 
        
                -- Random product_id between 1 and 5
                FLOOR(RAND() * 5) + 1, 
        
                -- Calculate the purchase date, increment by 1 for each row
                DATEADD(DAY, @i - 1, @start_date),
        
                -- Random quantity between 1 and 5
                FLOOR(RAND() * 5) + 1
            );
        
        SET @i = @i + 1;
    END
END;



-- 1. Insert Customers
INSERT INTO customers(customer_name, email_address, country)
VALUES 
    ('John Doe', 'johndoe@example.com', 'USA'),
    ('Jane Smith', 'janesmith@example.com', 'Canada'),
    ('Carlos Gonzalez', 'carlosg@example.com', 'Mexico'),
    ('Anna Lee', 'annalee@example.com', 'UK');


-- 2. Insert Products
INSERT INTO products (product_name, price, category)
VALUES 
    ('Laptop', 999.99, 'Electronics'),
    ('Smartphone', 499.99, 'Electronics'),
    ('Coffee Maker', 89.99, 'Home Appliances'),
    ('Wireless Mouse', 19.99, 'Electronics'),
    ('Winter Jacket', 59.99, 'Clothing');


-- 3. Insert Sales Transactions
INSERT INTO sales_transactions (customer_id, product_id, purchase_date, quantity)
VALUES 
    (1, 1, '2024-11-01', 1),  -- John Doe buys 1 Laptop
    (1, 2, '2024-11-02', 2),  -- John Doe buys 2 Smartphones
    (2, 3, '2024-11-03', 1),  -- Jane Smith buys 1 Coffee Maker
    (3, 4, '2024-11-04', 3),  -- Carlos Gonzalez buys 3 Wireless Mice
    (4, 5, '2024-11-05', 1);  -- Anna Lee buys 1 Winter Jacket


-- 4. Insert Shipping Details
INSERT INTO shipping_details (transaction_id, shipping_date, shipping_address, city, country)
VALUES 
    (1, '2024-11-02', '123 Main St, Apt 4B', 'New York', 'USA'),  -- Shipping for John Doe's Laptop
    (2, '2024-11-03', '123 Main St, Apt 4B', 'New York', 'USA'),  -- Shipping for John Doe's Smartphones
    (3, '2024-11-04', '456 Maple Ave', 'Toronto', 'Canada'),      -- Shipping for Jane Smith's Coffee Maker
    (4, '2024-11-06', '789 Oak Dr', 'Mexico City', 'Mexico'),     -- Shipping for Carlos Gonzalez's Wireless Mice
    (5, '2024-11-07', '321 Pine Ln', 'London', 'UK');             -- Shipping for Anna Lee's Winter Jacket


EXEC InsertRandomSalesTransactions;
