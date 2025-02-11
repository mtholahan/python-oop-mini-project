class Customer:
    def __init__(self, customer_id: int, first_name: str, last_name: str, address: str):
        self._customer_id = customer_id
        self._first_name = first_name
        self._last_name = last_name
        self._address = address
        self._accounts = []  # List of associated BankAccount objects

    def add_account(self, account):
        """Links a new bank account to this customer."""
        self._accounts.append(account)

    def get_account(self, account_number: str):
        """Retrieves a specific account by account number."""
        return next((account for account in self._accounts if account.account_number == account_number), None)

    # Getters for encapsulated attributes
    @property
    def customer_id(self):
        return self._customer_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def address(self):
        return self._address

    @property
    def accounts(self):
        return self._accounts