import sys
import db
from account import BankAccount
from customer import Customer

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
    """Handles user input for creating a new customer"""
    print("\n[Creating New Customer]")

    try:
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        email = input("Enter email: ").strip()
        phone = input("Enter phone number: ").strip()

        # Create a Customer object and save to DB
        customer = Customer(first_name, last_name, email, phone)
        customer.save_to_db()  # Saves and assigns a customer_id

        print(f"Customer {customer.first_name} {customer.last_name} created successfully with ID {customer.customer_id}.")
        print(f"Email: {customer.email}, Phone: {customer.phone}")

    except ValueError as e:
        print(f"Error: {e}")


def open_account():
    """Handles user input for opening a new account"""
    print("\n[Opening New Account]")
    customer_id = input("Enter your Customer ID: ").strip()

    if not customer_id.isdigit():
        print("Invalid Customer ID.")
        return

    customer = Customer.get_by_id(int(customer_id))
    if not customer:
        print("Customer not found. Please create a customer first.")
        return

    print(f"✅ Customer found: {customer.first_name} {customer.last_name}")

    account_type = input("Enter account type (Checking/Savings): ").strip().capitalize()
    if account_type not in ["Checking", "Savings"]:
        print("Invalid account type. Please enter 'Checking' or 'Savings'.")
        return

    initial_balance = input("Enter initial deposit amount: ").strip()
    if not initial_balance.replace('.', '', 1).isdigit():
        print("Invalid deposit amount.")
        return

    initial_balance = float(initial_balance)

    # Create and save the account
    new_account = BankAccount(customer.customer_id, account_type, initial_balance)
    new_account.save_to_db()

    print(f"✅ {account_type} account created successfully with balance ${initial_balance:.2f}.")


def deposit_funds():
    """Handles deposits through the CLI"""
    print("\n[Depositing Funds]")
    account_id = input("Enter Account ID: ").strip()
    account = BankAccount.get_by_id(int(account_id))
    if not account:
        print("Account not found.")
        return

    amount = input("Enter deposit amount: ").strip()
    if not amount.replace('.', '', 1).isdigit():
        print("Invalid deposit amount.")
        return

    amount = float(amount)

    try:
        account.deposit(amount)
        print(f"✅ Deposited ${amount:.2f} into Account {account_id}.")
    except ValueError as e:
        print(f"❌ {e}")


def withdraw_funds():
    """Handles withdrawals through the CLI"""
    print("\n[Withdrawing Funds]")
    account_id = input("Enter Account ID: ").strip()
    account = BankAccount.get_by_id(int(account_id))
    if not account:
        print("❌ Account not found.")
        return

    amount = input("Enter withdrawal amount: ").strip()
    if not amount.replace('.', '', 1).isdigit():
        print("❌ Invalid withdrawal amount.")
        return

    amount = float(amount)

    try:
        account.withdraw(amount)
        print(f"✅ Withdrew ${amount:.2f} from Account {account_id}.")
    except ValueError as e:
        print(f"❌ {e}")


def transfer_funds():
    """Handles fund transfers through the CLI"""
    print("\n[Transferring Funds]")
    sender_id = input("Enter source Account ID: ").strip()
    recipient_id = input("Enter destination Account ID: ").strip()
    amount = input("Enter transfer amount: ").strip()

    if not (sender_id.isdigit() and recipient_id.isdigit() and amount.replace('.', '', 1).isdigit()):
        print("❌ Invalid input. Please enter valid numbers.")
        return

    sender_id, recipient_id = int(sender_id), int(recipient_id)
    amount = float(amount)

    sender_account = BankAccount.get_by_id(sender_id)
    if not sender_account:
        print(f"❌ Sender Account {sender_id} not found.")
        return

    try:
        sender_account.transfer(recipient_id, amount)
        print(f"✅ Transferred ${amount:.2f} from Account {sender_id} to Account {recipient_id}.")
    except ValueError as e:
        print(f"❌ {e}")


def view_transaction_history():
    """Displays transaction history for an account."""
    print("\n[Viewing Transaction History]")

    account_id = input("Enter Account ID: ").strip()

    if not account_id.isdigit():
        print("❌ Invalid input. Please enter a numeric Account ID.")
        return

    transactions = db.get_transaction_history(int(account_id))

    if not transactions:
        print(f"ℹ️ No transactions found for Account {account_id}.")
        return

    print("\nTransaction History:")
    print("--------------------------------------------------")
    print(f"{'ID':<5} {'Type':<12} {'Amount':<10} {'Timestamp'}")
    print("--------------------------------------------------")

    for txn in transactions:
        txn_id, txn_type, amount, timestamp = txn
        print(f"{txn_id:<5} {txn_type:<12} ${amount:<9} {timestamp}")

    print("--------------------------------------------------")


def get_account(account_id):
    """Retrieve an account from the database and return a BankAccount object."""
    account_data = db.get_account(account_id)  # Fetch from database
    if not account_data:
        print("❌ Account not found.")
        return None

    # Corrected parameter order
    customer_id, account_type, balance, account_id = account_data
    return BankAccount(customer_id, account_type, balance, account_id)


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
            print("\n❌ Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
