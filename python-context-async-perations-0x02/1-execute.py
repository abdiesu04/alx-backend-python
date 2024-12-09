from mysql.connector import Error
from seed import Seed

class DatabaseConnection:
    """
    Context manager for database connection using the Seed class.
    """
    def __enter__(self):
        self.conn = Seed.connect_to_prodev()
        if self.conn is None:
            raise Exception("Failed to connect to the database.")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.conn.rollback()
            print(f"Transaction rolled back due to an error: {exc_val}")
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()


class ExecuteQuery:
    """
    Custom context manager to execute a query with parameters.
    """
    def __init__(self, connection, query, params):
        self.connection = connection
        self.query = query
        self.params = params

    def __enter__(self):
        try:
            self.cursor = self.connection.cursor(dictionary=True)  # Return results as dictionaries
            self.cursor.execute(self.query, self.params)
            return self.cursor
        except Error as err:
            print(f"Error during query execution: {err}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.rollback()
            print(f"Transaction rolled back due to an error: {exc_val}")
        else:
            self.connection.commit()
        self.cursor.close()


def main():
    """
    Main function to execute the query and print the results.
    """
    query = "SELECT * FROM user_data WHERE age > %s"
    params = (60,)

    # Using DatabaseConnection context manager
    with DatabaseConnection() as cursor:
        connection = cursor.connection  # Access the active connection
        # Using ExecuteQuery context manager
        with ExecuteQuery(connection, query, params) as exec_cursor:
            if exec_cursor:
                results = exec_cursor.fetchall()
                for row in results:
                    print(row)


if __name__ == "__main__":
    main()
