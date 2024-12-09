from seed import Seed

class DatabaseConnection:
    def __enter__(self):
        self.conn = Seed.connect_to_prodev()
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
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM user_data")
        results = cursor.fetchall()
        for row in results:
            print(row)
