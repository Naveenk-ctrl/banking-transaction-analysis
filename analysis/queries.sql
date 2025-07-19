-- 1.showing total number of students
SELECT COUNT(*) AS total_customers FROM Customers;
-- 2. list all customers with total  balance

SELECT c.CustomerID, c.Name, SUM(a.Balance) AS total_balance
FROM Customers c
JOIN Accounts a ON c.CustomerID = a.CustomerID
GROUP BY c.CustomerID;

--  3. Get Top 5 Customers by Total Debit Spent

SELECT c.CustomerID, c.Name, SUM(t.Amount) AS total_debit
FROM Customers c
JOIN Accounts a ON c.CustomerID = a.CustomerID
JOIN Transactions t ON a.AccountID = t.AccountID
WHERE t.TransactionType = 'debit'
GROUP BY c.CustomerID
ORDER BY total_debit DESC
LIMIT 5;

--  4. Monthly Transaction Summary

SELECT DATE_FORMAT(Timestamp, '%Y-%m') AS Month,
       TransactionType,
       COUNT(*) AS total_transactions,
       SUM(Amount) AS total_amount
FROM Transactions
GROUP BY Month, TransactionType
ORDER BY Month;

-- 5. Average Transaction Amount by Type

SELECT TransactionType, AVG(Amount) AS avg_amount
FROM Transactions
GROUP BY TransactionType;

-- 6. Detect Suspiciously High Transactions (e.g., > ₹50,000)

SELECT * FROM Transactions
WHERE Amount > 50000
ORDER BY Amount DESC;

-- 7. account with highest balance
SELECT a.AccountID, c.Name, a.Balance
FROM Accounts a
JOIN Customers c ON a.CustomerID = c.CustomerID
ORDER BY a.Balance DESC
LIMIT 1;


-- fraud detection


SELECT t.TransactionID, c.Name, t.Amount, t.TransactionType, t.Timestamp, t.Description
FROM Transactions t
JOIN Accounts a ON t.AccountID = a.AccountID
JOIN Customers c ON a.CustomerID = c.CustomerID
WHERE t.Amount > 50000
   OR HOUR(t.Timestamp) BETWEEN 0 AND 5
ORDER BY t.Timestamp DESC;


-- Recent Transactions (last 10)
SELECT t.TransactionID, c.Name, t.Amount, t.TransactionType, t.Timestamp, t.Description
FROM Transactions t
JOIN Accounts a ON t.AccountID = a.AccountID
JOIN Customers c ON a.CustomerID = c.CustomerID
ORDER BY t.Timestamp DESC
LIMIT 10;

SELECT t.TransactionID, c.Name, t.Amount, t.TransactionType, t.Timestamp, t.Description
FROM Transactions t
JOIN Accounts a ON t.AccountID = a.AccountID
JOIN Customers c ON a.CustomerID = c.CustomerID
WHERE t.Timestamp BETWEEN %s AND %s
ORDER BY t.Timestamp DESC;

SELECT c.Name, SUM(a.Balance) as TotalBalance
FROM Accounts a
JOIN Customers c ON a.CustomerID = c.CustomerID
GROUP BY c.CustomerID
ORDER BY TotalBalance DESC
LIMIT 5;


SELECT TransactionType, COUNT(*) as Count
FROM Transactions
GROUP BY TransactionType;


SELECT c.Name, DATE_FORMAT(t.Timestamp, '%Y-%m') as Month, SUM(t.Amount) as Total
FROM Transactions t
JOIN Accounts a ON t.AccountID = a.AccountID
JOIN Customers c ON a.CustomerID = c.CustomerID
WHERE t.TransactionType = 'debit'
GROUP BY c.Name, Month
ORDER BY Month;
