class Bank:
    def __init__(self, name: str):
        self._name = name
        self._customers = []  # Store customer objects
        self._accounts = [] # Store account objects

    def add_customer(self, customer):
        """Adds a new customer to the bank."""
        self._customers.append(customer)

    def add_account(self, account):
        """Adds a new account to the bank."""
        self._accounts.append(account)

    def get_customer_by_id(self, customer_id: int):
        """Retrieves a customer by their unique ID."""
        return next((cust for cust in self._customers if cust.customer_id == customer_id), None)
    
    def get_account_by_id(self, account_number: str):
        """Retrieves an account by its unique ID."""
        return next((account for account in self._accounts if account.number_number == account_number), None)
    
