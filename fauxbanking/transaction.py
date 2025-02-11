class Transaction:
    def __init__(self, transaction_id: int, account, transaction_type: str, amount: float, timestamp):
        self._transaction_id = transaction_id
        self._account = account # Associated BankAccount
        self._transaction_type = transaction_type # 'Deposit', 'Withdrawal', or 'Transfer'
        self._amount = amount
        self._timestamp = timestamp # e.g., datetime.now()

    def get_transaction_details(self):
        """Returns a summary of the transaction"""
        return f"{self._transaction_type} of ${self._amount} on {self._timestamp} for account {self._account.account_number}"
    