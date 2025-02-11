class BankAccount:
    def __init__(self, account_number: str, account_type: str, balance: float, customer):
        self._account_number = account_number
        self._account_type = account_type
        self._balance = balance
        self._customer = customer
    
    def deposit(self, amount: float):
        """Deposits a specific amount into the account"""
        if amount > 0:
            self._balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")
        
    def withdrawal(self, amount: float):
        """Withdrawals a specific amount from the account if sufficient funds exist"""
        if 0 < amount <= self._balance:
            self._balance -= amount
        else:
            raise ValueError("Insufficient funds or invalid withdrawal amount.")
        
    def transfer(self, to_account, amount: float):
        """Transfers a specified amount to another account if sufficient funds exist"""
        if 0 < amount <= self._balance:
            self.withdrawal(amount)
            to_account.deposit(amount)
        else:
            raise ValueError("Insufficient funds or invalid transfer amount.")
        
    # Getters for encapsulated attributes
    @property
    def account_number(self):
        return self._account_number
    
    @property
    def account_type(self):
        return self._account_type
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def customer(self):
        return self._customer
