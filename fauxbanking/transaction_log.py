class TransactionLog:
    def __init__(self, log_id: int, transaction: Transaction, log_message: str):
        self._log_id = log_id
        self._transaction_id = transaction.transaction_id # Linked to Transaction ID
        self._account_number = transaction.account.account_number # Associated account number
        self._log_message = log_message
        self._timestamp = transaction.timestamp # Timestamp from the transaction

    def get_log_details(self):
        """Returns a detailed log entry"""
        return f"Log ID: {self._log_id}, Transaction: {self._transaction_id}, Account: {self._account_number}, Message: {self._log_message}, Timestamp: {self._timestamp}"
    