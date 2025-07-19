from faker import Faker
import random
import mysql.connector
from datetime import datetime

fake = Faker()

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Naveen@123",  # change this
    database="BankingSystem"
)
cursor = db.cursor()

account_types = ['Savings', 'Current', 'Fixed Deposit']

# Add customers
# Add customers
customer_ids = []
for _ in range(10):
    name = fake.name()
    email = fake.email()
    phone = fake.msisdn()[:15]  # Ensures phone is max 15 characters
    address = fake.address().replace("\n", ", ")

    cursor.execute(
        "INSERT INTO Customers (Name, Email, Phone, Address) VALUES (%s, %s, %s, %s)",
        (name, email, phone, address)
    )
    customer_ids.append(cursor.lastrowid)


# Add accounts
account_ids = []
for customer_id in customer_ids:
    for _ in range(random.randint(1, 2)):
        account_type = random.choice(account_types)
        balance = round(random.uniform(1000, 100000), 2)
        created_date = fake.date_time_between(start_date='-2y', end_date='now')
        cursor.execute("INSERT INTO Accounts (CustomerID, AccountType, Balance, CreatedDate) VALUES (%s, %s, %s, %s)", 
                       (customer_id, account_type, balance, created_date))
        account_ids.append(cursor.lastrowid)

# Add transactions
for account_id in account_ids:
    for _ in range(random.randint(20, 50)):
        amount = round(random.uniform(100, 50000), 2)
        txn_type = random.choice(['credit', 'debit'])
        timestamp = fake.date_time_between(start_date='-1y', end_date='now')
        desc = fake.sentence()
        cursor.execute("INSERT INTO Transactions (AccountID, Amount, TransactionType, Timestamp, Description) VALUES (%s, %s, %s, %s, %s)", 
                       (account_id, amount, txn_type, timestamp, desc))

db.commit()
cursor.close()
db.close()
print("✅ Fake data inserted successfully!")
