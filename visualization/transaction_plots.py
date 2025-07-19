import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Naveen@123",     # ← Replace with your MySQL password
    database="BankingSystem"
)

# Define helper function to run query
def fetch_df(query):
    return pd.read_sql(query, conn)


# 1. Monthly Credit vs Debit Trend
monthly_query = """
SELECT DATE_FORMAT(Timestamp, '%Y-%m') AS Month,
       SUM(CASE WHEN TransactionType = 'credit' THEN Amount ELSE 0 END) AS Credit,
       SUM(CASE WHEN TransactionType = 'debit' THEN Amount ELSE 0 END) AS Debit
FROM Transactions
GROUP BY Month
ORDER BY Month;
"""

df = fetch_df(monthly_query)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['Month'], df['Credit'], label='Credit', marker='o')
plt.plot(df['Month'], df['Debit'], label='Debit', marker='o')
plt.title('Monthly Transaction Trends')
plt.xlabel('Month')
plt.ylabel('Total Amount (₹)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()


# 2. Top 5 Customers by Total Debit Spending
top_debit_query = """
SELECT c.Name, SUM(t.Amount) AS TotalDebit
FROM Customers c
JOIN Accounts a ON c.CustomerID = a.CustomerID
JOIN Transactions t ON a.AccountID = t.AccountID
WHERE t.TransactionType = 'debit'
GROUP BY c.Name
ORDER BY TotalDebit DESC
LIMIT 5;
"""

df_top_debit = fetch_df(top_debit_query)


# Plotting Top 5 Debit Customers
plt.figure(figsize=(10, 6))
plt.barh(df_top_debit['Name'], df_top_debit['TotalDebit'], color='orange')
plt.xlabel('Total Debit Spent (₹)')
plt.title('Top 5 Customers by Debit Spending')
plt.gca().invert_yaxis()  # Highest spender at the top
plt.grid(True, axis='x')
plt.tight_layout()
plt.show()


# 3. Total Credit vs Debit – Pie Chart
credit_debit_query = """
SELECT TransactionType, SUM(Amount) AS Total
FROM Transactions
GROUP BY TransactionType;
"""

df_credit_debit = fetch_df(credit_debit_query)

# Plot Pie Chart
plt.figure(figsize=(6, 6))
plt.pie(
    df_credit_debit['Total'],
    labels=df_credit_debit['TransactionType'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['#00c853', '#d50000']
)
plt.title('Total Credit vs Debit Distribution')
plt.axis('equal')  # Equal aspect ratio ensures it's a circle
plt.tight_layout()
plt.show()
