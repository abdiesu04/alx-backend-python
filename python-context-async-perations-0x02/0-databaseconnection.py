import mysql.connector

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pass1234!",
            database=self.db_name
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    db_name = 'ALX_prodev'
    with DatabaseConnection(db_name) as cursor:
        cursor.execute("SELECT * FROM user_data")
        results = cursor.fetchall()
        for row in results:
            print(row)