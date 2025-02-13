import sys
import db
from account import BankAccount

def display_menu():
    """Display the main menu."""
    print("\n=== Faux Banking System ===")
    print("1. Create Customer")
    print("2. Open Account")
    print("3. Deposit Funds")
    print("4. Withdraw Funds")
    print("5. Transfer Funds")
    print("6. View Transaction History")
    print("7. Exit")

def create_customer():
    """Prompt user for customer details and store in database."""
    print("\n[Create a New Customer]")
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone number (optional): ").strip() or None
    result = db.create_customer(first_name, last_name, email, phone)
    print(result)

def open_account():
    """Open a new account for an existing customer."""
    print("\n[Opening a New Account]")
    customer_id = input("Enter Customer ID: ").strip()
    account_type = input("Enter Account Type (Checking/Savings): ").strip().capitalize()
    if account_type not in ["Checking", "Savings"]:
        print("Invalid account type. Please enter 'Checking' or 'Savings'.")
        return

    result = db.create_account(customer_id, account_type)
    print(result)

def get_account(account_id):
    """Retrieve an account from the database and return a BankAccount object."""
    account_data = db.get_account(account_id)  # Fetch from database
    if not account_data:
        print("Account not found.")
        return None

    account_id, account_type, balance, customer_id = account_data
    return BankAccount(account_id, account_type, balance, customer_id)

def deposit_funds():
    """Handles depositing funds into an account."""
    print("\n[Depositing Funds]")
    account_id = input("Enter Account ID: ").strip()
    account = get_account(account_id)
    if not account:
        return

    amount = input("Enter deposit amount: ").strip()
    try:
        amount = float(amount)
        if amount <= 0:
            print("Invalid amount. Must be a positive number.")
            return
    except ValueError:
        print("Invalid input. Please enter a numerical amount.")
        return

    result = account.deposit(amount)
    print(result)

def withdraw_funds():
    """Handles withdrawing funds from an account."""
    print("\n[Withdrawing Funds]")
    account_id = input("Enter Account ID: ").strip()
    account = get_account(account_id)
    if not account:
        return

    amount = input("Enter withdrawal amount: ").strip()
    try:
        amount = float(amount)
        if amount <= 0:
            print("Invalid amount. Must be a positive number.")
            return
    except ValueError:
        print("Invalid input. Please enter a numerical amount.")
        return

    result = account.withdraw(amount)
    print(result)

def transfer_funds():
    """Handles transferring funds between two accounts."""
    print("\n[Transferring Funds]")
    from_account_id = input("Enter Sender Account ID: ").strip()
    to_account_id = input("Enter Receiver Account ID: ").strip()

    if from_account_id == to_account_id:
        print("Cannot transfer funds to the same account.")
        return

    from_account = get_account(from_account_id)
    to_account = get_account(to_account_id)

    if not from_account or not to_account:
        return

    amount = input("Enter transfer amount: ").strip()
    try:
        amount = float(amount)
        if amount <= 0:
            print("Invalid amount. Must be a positive number.")
            return
    except ValueError:
        print("Invalid input. Please enter a numerical amount.")
        return

    result = from_account.transfer(to_account_id, amount)
    print(result)

def view_transaction_history():
    """Displays transaction history for an account."""
    print("\n[Viewing Transaction History]")

    account_id = input("Enter Account ID: ").strip()

    # Ensure account_id is a valid integer
    if not account_id.isdigit():
        print("Invalid input. Please enter a numeric Account ID.")
        return

    transactions = db.get_transaction_history(int(account_id))

    if isinstance(transactions, str):  # Check for error message from db.py
        print(transactions)
        return

    if not transactions:  # Handle case where no transactions exist
        print(f"No transactions found for Account {account_id}.")
        return

    # Display transaction history in a readable format
    print("\nTransaction History:")
    print("--------------------------------------------------")
    print(f"{'ID':<5} {'Type':<12} {'Amount':<10} {'Timestamp'}")
    print("--------------------------------------------------")

    for txn in transactions:
        txn_id, txn_type, amount, timestamp = txn
        print(f"{txn_id:<5} {txn_type:<12} ${amount:<9} {timestamp}")

    print("--------------------------------------------------")



def main():
    """Main loop for the CLI."""
    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            create_customer()
        elif choice == "2":
            open_account()
        elif choice == "3":
            deposit_funds()
        elif choice == "4":
            withdraw_funds()
        elif choice == "5":
            transfer_funds()
        elif choice == "6":
            view_transaction_history()
        elif choice == "7":
            print("\nExiting Faux Banking System. Goodbye!")
            sys.exit()
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
