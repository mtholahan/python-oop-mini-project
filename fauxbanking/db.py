import os
from dotenv import load_dotenv
import pyodbc

# Load variables from .env
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    """Establish a connection to the Azure SQL database."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};DATABASE={DB_NAME};"
            f"UID={DB_USER};PWD={DB_PASSWORD}"
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def create_customer(first_name, last_name, email, phone):
    """Insert a new customer into the database."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber)
                VALUES (?, ?, ?, ?)
                """,
                (first_name, last_name, email, phone),
            )
            conn.commit()
            print("Customer created successfully!")
        except Exception as e:
            print(f"Error inserting customer: {e}")
        finally:
            conn.close()

def create_account(customer_id, account_type):
    """Creates a new bank account for a customer"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Account(CustomerID, AccountType, Balance)
                VALUES (?, ?, ?)
                """,
                (customer_id, account_type, 0.00) # Start with a $0 balance
            )
            conn.commit()
            print(f"Account created successfully for Customer ID {customer_id}.")
        except Exception as e:
            print(f"Error creating account: {e}.")
        finally:
            conn.close()