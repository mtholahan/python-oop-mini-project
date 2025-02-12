import pyodbc

server = 'fbs-sql-server.database.windows.net'
database = 'FauxBankingSystemDB'
username = 'admin_fbs'
password = '4ucrU9a&rAy5*it&o@@O'

try:
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    print("Connected successfully!")
except Exception as e:
    print("Connection failed:", e)
