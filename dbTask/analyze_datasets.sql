-- Calculate the total sales amount and the total number of transactions for each month. 

SELECT 
    YEAR(st.purchase_date) AS year,
    MONTH(st.purchase_date) AS month,
    COUNT(st.transaction_id) AS total_transactions,      -- Total number of transactions
    SUM(st.quantity * p.price) AS total_sales_amount     -- Total sales amount 
FROM 
    sales_transactions st
JOIN 
    products p ON st.product_id = p.product_id          -- Join sales transactions with products to get price
GROUP BY 
    YEAR(st.purchase_date),                             -- Group by year
    MONTH(st.purchase_date)                             -- Group by month
ORDER BY 
    YEAR(st.purchase_date) ASC,                         
    MONTH(st.purchase_date) ASC;                       




-- Calculate the 3-month moving average of sales amount for each month.

WITH MonthlySales AS (
    -- Calculate total sales per month
    SELECT 
        YEAR(st.purchase_date) AS year,
        MONTH(st.purchase_date) AS month,
        SUM(st.quantity * p.price) AS total_sales
    FROM 
        sales_transactions st
    JOIN 
        products p ON st.product_id = p.product_id
    GROUP BY 
        YEAR(st.purchase_date),
        MONTH(st.purchase_date)
)

SELECT 
    ms.year,
    ms.month,
    ms.total_sales,

    -- Calculate the 3-month moving average using current and 2 previous rows
    AVG(ms.total_sales) OVER (
        ORDER BY ms.year, ms.month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS three_month_moving_avg

FROM 
    MonthlySales ms
ORDER BY 
    ms.year, ms.month;
 