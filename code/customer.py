from db import get_db_connection, log_event
import re

class Customer:
    def __init__(self, first_name, last_name, email, phone, customer_id=None):
        """Initialize a Customer object with private attributes"""
        self._customer_id = customer_id
        self._first_name = None  # Will be set using setter
        self._last_name = None
        self._email = None
        self._phone = None

        self.first_name = first_name  # Calls setter for validation
        self.last_name = last_name
        self.email = email
        self.phone = phone

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value.isalpha():
            raise ValueError("First name must contain only letters.")
        self._first_name = value.strip().capitalize()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value.isalpha():
            raise ValueError("Last name must contain only letters.")
        self._last_name = value.strip().capitalize()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        """Validate email format using regex"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format.")
        self._email = value.strip().lower()

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        """Ensure phone contains only numbers and is 10-15 digits long"""
        if not value.isdigit() or not (10 <= len(value) <= 15):
            raise ValueError("Phone number must be 10-15 digits long.")
        self._phone = value.strip()

    def save_to_db(self):
        """Saves the customer to the database and assigns a CustomerID"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber) VALUES (?, ?, ?, ?)",
            (self._first_name, self._last_name, self._email, self._phone),
        )

        # Retrieve the new CustomerID
        cursor.execute("SELECT @@IDENTITY")
        self._customer_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        # Log the event
        log_message = f"New customer created: {self._first_name} {self._last_name}, ID {self._customer_id}, Email: {self._email}, Phone: {self._phone}"
        log_event("INFO", log_message)

    @classmethod
    def get_by_id(cls, customer_id):
        """Retrieves a customer from the database by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT CustomerID, FirstName, LastName, Email, PhoneNumber FROM Customer WHERE CustomerID = ?", (customer_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(row[1], row[2], row[3], row[4], row[0])  # Return a Customer object
        else:
            return None  # No customer found
