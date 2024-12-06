import mysql.connector
from seed import Seed
from functools import wraps

# Decorator for logging
def logqueries(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        print("Pre logging")
        res  = fun(*args, **kwargs)
        return res
        print("Post logging")
    return wrapper

@logqueries
def fetch_all_users(queries):
    connection = Seed.connect_to_prodev()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries)
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row  # Yielding rows from the database
    except mysql.connector.Error as err:
        print(f"Error fetching user data: {err}")
    finally:
        cursor.close()
        connection.close()

# Call the generator function
users = fetch_all_users("SELECT * FROM user_data")
for user in users:
    print(user)
