# Python OOP Mini Project


## 📖 Abstract
This project implements a simplified banking system using Python object-oriented programming (OOP) principles, with a focus on modular design, class hierarchies, and UML modeling. The system models core banking entities such as customers, accounts, employees, loans, and credit cards, each with their own attributes and behaviors.

Key features include:

* Customer class with fields for first name, last name, and address.

* Account class supporting checking and savings accounts, with deposit, withdrawal, and balance tracking methods.

* Support for financial services such as loans and credit cards, implemented as additional classes.

* Input handling through a command-line interface, allowing users to perform account operations interactively.

* Error handling with Python exceptions to ensure the program responds gracefully to invalid operations.

* Logging to both the console and a log file for runtime monitoring.

A UML class diagram captures the system’s overall design, illustrating relationships among entities, while PEP-8 style and structured project organization ensure maintainability. The project deliverables include the UML diagram, Python source code, and a README file describing the system design and functionality.

This project provided hands-on practice with OOP design, UML class diagrams, error handling, and Python CLI development, while simulating real-world considerations in building financial applications



## 🛠 Requirements
- Python 3.8+
- Adherence to PEP-8 style guide
- UML diagram of class design
- Logging implemented (console + file)
- Exception handling implemented
- README.md explaining design
- Libraries: python-dotenv, pyodbc (from requirements.txt)



## 🧰 Setup
- Clone repo and create virtual environment
- pip install -r requirements.txt
- Ensure logs/ folder exists for runtime error/warning capture
- Run Python scripts directly from command line (see Run Steps)



## 📊 Dataset
- Data persistence can vary:
  - Recommended: JSON or CSV files for storing accounts/customers
  - Optionally: SQLite or SQL Server (via pyodbc)
  - In-memory structures possible (not recommended for persistence)



## ⏱️ Run Steps
- Launch program from CLI:
  python main.py
- Follow interactive prompts to:
  - Create customers/accounts
  - Perform deposits/withdrawals
  - Request balances, loans, or credit card services



## 📈 Outputs
- Interactive CLI output (account balances, transactions, etc.)
- Log files stored under logs/ capturing errors and warnings
- Generated UML diagram describing class structure



## 📸 Evidence

![uml_diagram.png](./evidence/uml_diagram.png)  
Screenshot of UML class diagram

![cli_session.png](./evidence/cli_session.png)  
Screenshot of CLI session showing deposit and withdrawal

![logs_example.png](./evidence/logs_example.png)  
Screenshot of log file contents (errors/warnings captured)




## 📎 Deliverables

- [`- Python source code implementing OOP banking system`](./deliverables/- Python source code implementing OOP banking system)

- [`- UML class diagram (PNG/PDF) in deliverables/`](./deliverables/- UML class diagram (PNG/PDF) in deliverables/)

- [`- requirements.txt`](./deliverables/- requirements.txt)

- [`- Raw application log: deliverables/log_oop.txt`](./deliverables/- Raw application log: deliverables/log_oop.txt)

- [`- README.md explaining design and usage`](./deliverables/- README.md explaining design and usage)




## 🛠️ Architecture
- Object-oriented Python design
- Classes: Customer, Account, Employee, Loan, CreditCard
- Responsibilities divided with getters/setters
- Relationships documented via UML diagram



## 🔍 Monitoring
- Logging of errors/warnings to console and file
- Manual verification of CLI operations and balances
- Optional: unit tests for deposit/withdraw logic



## ♻️ Cleanup
- Remove JSON/CSV test data (if used)
- Clear logs/ directory
- Deactivate and delete virtual environment



*Generated automatically via Python + Jinja2 + SQL Server table `tblMiniProjectProgress` on 09-14-2025 23:37:22*