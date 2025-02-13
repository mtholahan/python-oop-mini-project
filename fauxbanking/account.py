import db  # Import database functions
from decimal import Decimal

class BankAccount:
    def __init__(self, account_id: int, account_type: str, balance: float, customer):
        self._account_id = account_id
        self._account_type = account_type
        self._balance = balance
        self._customer = customer  # Customer object or customer_id

    # Read-only Property for Account ID (Cannot be Changed)
    @property
    def account_id(self):
        return self._account_id

    # Account Type Property (Optional Setter)
    @property
    def account_type(self):
        return self._account_type

    @account_type.setter
    def account_type(self, new_type: str):
        """Allows changing account type with validation."""
        if new_type not in ["Checking", "Savings"]:
            raise ValueError("Invalid account type. Must be 'Checking' or 'Savings'.")
        self._account_type = new_type  # Update in memory
        db.update_account_type(self._account_id, new_type)  # Ensure DB is updated

    # Read-only Property for Balance (Updated through Transactions)
    @property
    def balance(self):
        return self._balance

    # Read-only Property for Customer
    @property
    def customer(self):
        return self._customer

    # Deposit Method
    def deposit(self, amount: float):
        """Deposits a specific amount into the account and updates the database."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        result = db.deposit(self._account_id, Decimal(amount))  # Convert to decimal
        if "Deposited" in result:
            self._balance += Decimal(amount)  # Update object balance only if successful
        return result

    # Withdraw Method
    def withdraw(self, amount: float):
        """Withdraws a specific amount if sufficient funds exist and updates the database."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if self._balance < amount:
            return "Insufficient funds."

        result = db.withdraw(self._account_id, Decimal(amount))  # Centralized call to db.py
        if "Withdrew" in result:
            self._balance -= Decimal(amount)  # Update object balance only if successful
        return result

    # Transfer Method
    def transfer(self, to_account_id, amount: float):
        """Transfers funds to another account and updates the database."""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")

        if self._balance < amount:
            return "Insufficient funds."

        result = db.transfer(self._account_id, to_account_id, Decimal(amount))  # Centralized call to db.py
        if "Transferred" in result:
            self._balance -= Decimal(amount)  # Update sender balance only if successful
        return result
