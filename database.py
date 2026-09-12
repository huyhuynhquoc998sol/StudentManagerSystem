import pyodbc

class DatabaseConnection:
    def __init__(self):
        self.server = 'QUOC_HUY\\SQLEXPRESS' 
        self.database = 'StudentManagementSystem'
        self.conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"

    def connect(self):
        try:
            return pyodbc.connect(self.conn_str)
        except pyodbc.Error as e:
            print("Database connection error:", e)
            return None