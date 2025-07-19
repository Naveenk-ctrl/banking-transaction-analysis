from flask import Flask, render_template
import mysql.connector
import pandas as pd

app = Flask(__name__)

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Naveen@123",
    database="BankingSystem"
)



@app.route("/")
def dashboard():
    # 1. Top 5 Customers by Debit
    query1 = """
    SELECT c.Name, SUM(t.Amount) AS TotalDebit
    FROM Customers c
    JOIN Accounts a ON c.CustomerID = a.CustomerID
    JOIN Transactions t ON a.AccountID = t.AccountID
    WHERE t.TransactionType = 'debit'
    GROUP BY c.Name
    ORDER BY TotalDebit DESC
    LIMIT 5;
    """
    df_debit = pd.read_sql(query1, conn)

    # 2. Credit vs Debit Summary
    query2 = """
    SELECT TransactionType, SUM(Amount) AS Total
    FROM Transactions
    GROUP BY TransactionType;
    """
    df_total = pd.read_sql(query2, conn)

    # 3. Monthly Credit vs Debit Trend
    query3 = """
    SELECT DATE_FORMAT(Timestamp, '%Y-%m') AS Month,
           SUM(CASE WHEN TransactionType = 'credit' THEN Amount ELSE 0 END) AS Credit,
           SUM(CASE WHEN TransactionType = 'debit' THEN Amount ELSE 0 END) AS Debit
    FROM Transactions
    GROUP BY Month
    ORDER BY Month;
    """
    df_monthly = pd.read_sql(query3, conn)

    return render_template("dashboard.html",
                           top_spenders=df_debit.to_dict(orient='records'),
                           totals=df_total.to_dict(orient='records'),
                           monthly=df_monthly.to_dict(orient='records'))

@app.route("/fraud")
def fraud():
    fraud_query = """
    SELECT t.TransactionID, c.Name, t.Amount, t.TransactionType, t.Timestamp, t.Description
    FROM Transactions t
    JOIN Accounts a ON t.AccountID = a.AccountID
    JOIN Customers c ON a.CustomerID = c.CustomerID
    WHERE t.Amount > 50000
       OR HOUR(t.Timestamp) BETWEEN 0 AND 5
    ORDER BY t.Timestamp DESC;
    """
    df_fraud = pd.read_sql(fraud_query, conn)
    return render_template("fraud.html", fraud_transactions=df_fraud.to_dict(orient='records'))
@app.route("/recent")
def recent_transactions():
    recent_query = """
    SELECT t.TransactionID, c.Name, t.Amount, t.TransactionType, t.Timestamp, t.Description
    FROM Transactions t
    JOIN Accounts a ON t.AccountID = a.AccountID
    JOIN Customers c ON a.CustomerID = c.CustomerID
    ORDER BY t.Timestamp DESC
    LIMIT 10;
    """
    df_recent = pd.read_sql(recent_query, conn)
    return render_template("recent.html", recent=df_recent.to_dict(orient='records'))

from flask import request  # already imported render_template

@app.route("/filter", methods=["GET", "POST"])
def filter_transactions():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        filter_query = """
        SELECT t.TransactionID, c.Name, t.Amount, t.TransactionType, t.Timestamp, t.Description
        FROM Transactions t
        JOIN Accounts a ON t.AccountID = a.AccountID
        JOIN Customers c ON a.CustomerID = c.CustomerID
        WHERE t.Timestamp BETWEEN %s AND %s
        ORDER BY t.Timestamp DESC;
        """
        df_filtered = pd.read_sql(filter_query, conn, params=(start_date, end_date))

        return render_template("filter.html", transactions=df_filtered.to_dict(orient='records'),
                               start_date=start_date, end_date=end_date)

    return render_template("filter.html", transactions=[], start_date="", end_date="")



if __name__ == "__main__":
    app.run(debug=True)

   