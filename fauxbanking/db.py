import pyodbc

def get_db_connection():
    """Returns a connection to the Azure SQL database."""
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=your_server.database.windows.net;'
        'PORT=1433;'
        'DATABASE=your_database;'
        'UID=your_username;'
        'PWD=your_password'
    )
    return conn
