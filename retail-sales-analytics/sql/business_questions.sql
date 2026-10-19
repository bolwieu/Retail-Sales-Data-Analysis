-- SQLite compatible. Import outputs/cleaned_sales.csv as table sales.
-- 1. Revenue and profit by category
SELECT category, ROUND(SUM(revenue), 2) AS revenue, ROUND(SUM(profit), 2) AS profit
FROM sales GROUP BY category ORDER BY revenue DESC;

-- 2. Monthly sales trends
SELECT substr(order_date, 1, 7) AS month, ROUND(SUM(revenue), 2) AS revenue,
COUNT(DISTINCT order_id) AS orders
FROM sales GROUP BY substr(order_date, 1, 7) ORDER BY month;

-- 3. Top 10 customers by spend
SELECT customer_id, COUNT(DISTINCT order_id) AS orders, ROUND(SUM(revenue), 2) AS total_spend
FROM sales GROUP BY customer_id ORDER BY total_spend DESC LIMIT 10;

-- 4. Region-level profitability
SELECT region, ROUND(SUM(profit), 2) AS profit,
ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales GROUP BY region ORDER BY profit DESC;

-- 5. Product-level performance
SELECT product, SUM(quantity) AS units_sold, ROUND(SUM(revenue), 2) AS revenue
FROM sales GROUP BY product ORDER BY revenue DESC;
