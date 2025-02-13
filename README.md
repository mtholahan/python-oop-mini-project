# 💰 Faux Banking System (FBS)

## 📌 Overview
The **Faux Banking System (FBS)** is a **command-line banking application** that allows users to:
- **Create customer accounts**
- **Open bank accounts (Checking, Savings)**
- **Deposit, withdraw, and transfer funds**
- **View transaction history**
- **Log system events and transactions** (both in a **SQL database** and a **log file**)

This project is built using **Python, Object-Oriented Programming (OOP), and Azure SQL Server for data storage**.

---

## 🚀 Features
✅ **Command-line interface for easy interaction**
✅ **Secure transaction handling (deposits, withdrawals, transfers)**
✅ **SQL Server integration for persistent data storage**
✅ **Logging to both a database (`Log` table) and a file (`logs/banking.log`)**
✅ **Error handling for invalid transactions and database failures**

## 🛠️ Installation & Setup

### 1️⃣ **Clone the Repository**

git clone https://github.com/mtholahan/FauxBankingSystem.git
cd FauxBankingSystem

### 2️⃣ **Install Dependencies**
pip install -r requirements.txt

### 3️⃣ **Set Up Database Configuration**
Create a .env file in the project root with your Azure SQL Server credentials:
DB_SERVER=your_server.database.windows.net
DB_NAME=FauxBankingSystemDB
DB_USER=your_username
DB_PASSWORD=your_password

🎮 How to Run the CLI
Run the command-line interface: python cli.py

You will see:
=== Faux Banking System ===
1. Create Customer
2. Open Account
3. Deposit Funds
4. Withdraw Funds
5. Transfer Funds
6. View Transaction History
7. Exit
Select an option (1-7):

Simply select an option and follow the prompts.

📂 Project Structure
├── fauxbanking/
│   ├── cli.py             # CLI user interface
│   ├── db.py              # Database interaction logic
│   ├── account.py         # Account class
│   ├── customer.py        # Customer class
│   ├── transaction.py     # Transaction class
│   ├── transaction_log.py # Handles transaction history
│   ├── bank.py            # Core banking logic
│   ├── logs/              # Stores banking.log file
├── .env                   # Environment variables (DO NOT SHARE)
├── README.md              # Project documentation
├── requirements.txt       # Dependencies list


📝 Logging
✅ Transactions & errors are stored in logs/banking.log
✅ Database logs are stored in the Log table in SQL Server
✅ To check logs in the log file, use:

cat logs/banking.log  # macOS/Linux
type logs\banking.log  # Windows

✅ To view logs in the database, run:
SELECT * FROM Log ORDER BY LogTimestamp DESC;


📜 UML Diagram
The UML Diagram for this project was created and approved by the mentor. It represents:

    Customer (Has one or more Bank Accounts)
    BankAccount (Handles deposits, withdrawals, and transfers)
    TransactionLog (Stores all transactions)
    Log (Stores system logs)


⚠️ Error Handling
    If a deposit, withdrawal, or transfer fails, an error is logged.
    If a database connection fails, the CLI will notify the user and log the error.
    Insufficient funds prevent withdrawals and transfers.


🚀 Future Enhancements (Optional)

    ✅ Admin View for Logs (CLI Option to review logs)
    ✅ Export Transaction History to .csv
    ✅ Multi-User Authentication System
    ✅ Bank Statements Generation


📜 License

This project is licensed under the MIT License.

📧 Contact

For questions or feedback, contact Mark Holahan at markholahan@proton.me