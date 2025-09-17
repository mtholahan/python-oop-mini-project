from db import get_db_connection, log_event
from decimal import Decimal

class BankAccount:
    def __init__(self, customer_id, account_type, balance=0, account_id=None):
        """Initialize a BankAccount object with private attributes"""
        self._account_id = account_id
        self._customer_id = customer_id
        self._account_type = account_type
        self._balance = Decimal(balance)

    @property
    def account_id(self):
        return self._account_id

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def account_type(self):
        return self._account_type

    @property
    def balance(self):
        return self._balance

    def save_to_db(self):
        """Saves the account to the database and assigns an AccountID"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Account (CustomerID, AccountType, Balance) VALUES (?, ?, ?)",
            (self._customer_id, self._account_type, self._balance),
        )

        # Retrieve the new AccountID
        cursor.execute("SELECT @@IDENTITY")
        self._account_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        log_event("INFO", f"New {self._account_type} account created for Customer {self._customer_id}, Account ID: {self._account_id}, Balance: ${self._balance:.2f}")

    @classmethod
    def get_by_id(cls, account_id):
        """Retrieves an account from the database by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT AccountID, CustomerID, AccountType, Balance FROM Account WHERE AccountID = ?", (account_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(row[1], row[2], row[3], row[0])  # Return a BankAccount object
        else:
            return None  # No account found

    def deposit(self, amount):
        """Deposits a specified amount and logs transaction"""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Account SET Balance = Balance + ? WHERE AccountID = ?",
            (amount, self._account_id),
        )

        cursor.execute(
            "INSERT INTO TransactionLog (AccountID, TransactionType, Amount) VALUES (?, 'Deposit', ?)",
            (self._account_id, amount),
        )

        conn.commit()
        conn.close()

        self._balance += Decimal(amount)

        log_event("INFO", f"Deposited ${amount:.2f} into Account {self._account_id}")

    def withdraw(self, amount):
        """Withdraws a specified amount if sufficient balance exists and logs transaction"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if self._balance < amount:
            raise ValueError("Insufficient funds.")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Account SET Balance = Balance - ? WHERE AccountID = ?",
            (amount, self._account_id),
        )

        cursor.execute(
            "INSERT INTO TransactionLog (AccountID, TransactionType, Amount) VALUES (?, 'Withdrawal', ?)",
            (self._account_id, amount),
        )

        conn.commit()
        conn.close()

        self._balance -= Decimal(amount)

        log_event("INFO", f"Withdrew ${amount:.2f} from Account {self._account_id}")

    def transfer(self, recipient_account_id, amount):
        """Transfers funds to another account if sufficient balance exists"""
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")
        
        # Convert amount to Decimal
        amount = Decimal(amount)

        # Validate the recipient account
        recipient = BankAccount.get_by_id(recipient_account_id)
        if not recipient:
            raise ValueError(f"Recipient account {recipient_account_id} not found.")

        if self._balance < amount:
            raise ValueError("Insufficient funds for transfer.")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Withdraw from sender
            cursor.execute(
                "UPDATE Account SET Balance = Balance - ? WHERE AccountID = ?",
                (amount, self._account_id),
            )

            # Deposit into recipient
            cursor.execute(
                "UPDATE Account SET Balance = Balance + ? WHERE AccountID = ?",
                (amount, recipient_account_id),
            )

            # Log the transfer in TransactionLog
            cursor.execute(
                "INSERT INTO TransactionLog (AccountID, RelatedAccountID, TransactionType, Amount) VALUES (?, ?, 'Transfer', ?)",
                (self._account_id, recipient_account_id, amount),
            )

            cursor.execute(
                "INSERT INTO TransactionLog (AccountID, RelatedAccountID, TransactionType, Amount) VALUES (?, ?, 'Transfer', ?)",
                (recipient_account_id, self._account_id, amount),
            )

            conn.commit()  # Commit the transaction
            self._balance -= amount
            recipient._balance += amount

            log_event("INFO", f"Transferred ${amount:.2f} from Account {self._account_id} to Account {recipient_account_id}")

        except Exception as e:
            conn.rollback()  # Rollback if anything fails
            log_event("ERROR", f"Transfer failed from Account {self._account_id} to Account {recipient_account_id}: {e}")
            raise ValueError(f"Transfer failed: {e}")

        finally:
            conn.close()
