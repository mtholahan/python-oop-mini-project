import sys
import db # Import the database module

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
    db.create_customer(first_name, last_name, email, phone)

def open_account():
    """Placeholder function for opening an account."""
    print("\n[Opening a New Account]")
    customer_id = input("Enter Customer ID: ").strip()
    account_type = input("Enter Account Type (Checking/Savings): ").strip().capitalize()
    if account_type not in ["Checking", "Savings"]:
        print("Invalid account type. Please enter 'Checking' or 'Savings'.")
        return
    db.create_account(customer_id, account_type)

def deposit_funds():
    """Placeholder function for depositing funds."""
    print("\n[Depositing Funds] (Not yet implemented)")

def withdraw_funds():
    """Placeholder function for withdrawing funds."""
    print("\n[Withdrawing Funds] (Not yet implemented)")

def transfer_funds():
    """Placeholder function for transferring funds."""
    print("\n[Transferring Funds] (Not yet implemented)")

def view_transaction_history():
    """Placeholder function for viewing transaction history."""
    print("\n[Viewing Transaction History] (Not yet implemented)")

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
