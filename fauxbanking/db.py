import os
from dotenv import load_dotenv
import pyodbc
from decimal import Decimal
import logging

# Load variables from .env
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Ensure logs directory exists
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Configure logging to write to a file
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "banking.log"),  # Log file at project root logs/
    level=logging.INFO,            # log only INFO and higher levels
    format="%(asctime)s - %(levelname)s - %(message)s "
)


def get_db_connection():
    """Establish a connection to the Azure SQL database and force autocommit."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};DATABASE={DB_NAME};"
            f"UID={DB_USER};PWD={DB_PASSWORD}"
        )

        conn.autocommit = True  # **Force SQL Server to commit immediately**

        # Debug: Confirm connected database
        cursor = conn.cursor()
        cursor.execute("SELECT DB_NAME();")
        db_name = cursor.fetchone()[0]
        # print(f"DEBUG: Connected to database: {db_name}")  # Output the database name

        return conn
    except pyodbc.Error as e:
        raise ConnectionError(f"Database connection failed: {e}")


def create_customer(first_name, last_name, email, phone):
    """Insert a new customer into the database and return the Customer ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber)
            VALUES (?, ?, ?, ?);
            """,
            (first_name, last_name, email, phone),
        )

        # Retrieve the newly generated CustomerID
        cursor.execute("SELECT SCOPE_IDENTITY();")
        new_customer_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()
        return f"Customer created successfully with ID {new_customer_id}."
    except Exception as e:
        return f"Error inserting customer: {e}"


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


def deposit(account_id, amount):
    """Deposits funds into an account and logs the transaction."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update account balance
        cursor.execute(
            "UPDATE Account SET Balance = Balance + ? WHERE AccountID = ?",
            (Decimal(amount), account_id),
        )

        # Insert into TransactionLog
        cursor.execute(
            """
            INSERT INTO TransactionLog (AccountID, TransactionType, Amount)
            VALUES (?, 'Deposit', ?)
            """,
            (account_id, Decimal(amount)),
        )

        conn.commit()
        conn.close()

        # Log this event
        log_event("INFO", f"Deposit of ${amount:.2f} to Account {account_id}.")

        return f"Deposited ${amount:.2f} into account {account_id}."

    except Exception as e:
        log_event("ERROR", f"Deposit failed for Account {account_id}: {e}")
        return f"Error during deposit: {e}"



def withdraw(account_id, amount):
    """Withdraws funds from an account if balance allows and logs the transaction."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check current balance
        cursor.execute("SELECT Balance FROM Account WHERE AccountID = ?", (account_id,))
        row = cursor.fetchone()
        if not row:
            log_event("WARNING", f"Withdrawal attempt failed: Account {account_id} not found.")
            return "Account not found."
        
        current_balance = Decimal(row[0])
        if current_balance < Decimal(amount):
            log_event("WARNING", f"Insufficient funds for withdrawal from Account {account_id}.")
            return "Insufficient funds."

        # Update balance
        cursor.execute(
            "UPDATE Account SET Balance = Balance - ? WHERE AccountID = ?",
            (Decimal(amount), account_id),
        )

        # Insert into TransactionLog
        cursor.execute(
            """
            INSERT INTO TransactionLog (AccountID, TransactionType, Amount)
            VALUES (?, 'Withdrawal', ?)
            """,
            (account_id, Decimal(amount)),
        )

        conn.commit()
        conn.close()

        # Log this event
        log_event("INFO", f"Withdrawal of ${amount:.2f} from Account {account_id}.")

        return f"Withdrew ${amount:.2f} from account {account_id}."

    except Exception as e:
        log_event("ERROR", f"Withdrawal failed for Account {account_id}: {e}")
        return f"Error during withdrawal: {e}"



def get_account(account_id):
    """Fetch account details from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT AccountID, AccountType, Balance, CustomerID FROM Account WHERE AccountID = ?",
            (account_id,)
        )
        account_data = cursor.fetchone()  # Fetch the first row

        conn.close()

        return account_data  # This will be a tuple if an account is found, or None if not
    except Exception as e:
        print(f"Error retrieving account: {e}")
        return None
    
def get_transaction_history(account_id):
    """Retrieves transaction history for a given account."""

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get transactions, most recent first
        cursor.execute(
            """
            SELECT TransactionID, TransactionType, Amount, TransactionTimeStamp
            FROM TransactionLog
            WHERE AccountID = ?
            ORDER BY TransactionTimeStamp DESC
            """,
            (account_id),
        )

        transactions = cursor.fetchall()

        conn.close()
        return transactions # Return the goods

    except Exception as e:
        return f"Error getting transaction history: {e}"


def log_event(log_level, message):
    """Logs an event into the Log table."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Log (LogLevel, Message)
            VALUES (?, ?)
            """,
            (log_level, message),
        )

        # Also log to the banking.log file
        if log_level == "ERROR":
            logging.error(message)
        elif log_level == "WARNING":
            logging.warning(message)
        else:
            logging.info(message)

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging event: {e}")  # Fallback in case logging fails
