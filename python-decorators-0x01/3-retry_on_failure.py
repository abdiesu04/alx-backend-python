import time
from seed import Seed

# Decorator to manage database connections
def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = Seed.connect_to_prodev()
        try:
            return func(connection, *args, **kwargs)
        finally:
            connection.close()
    return wrapper

# Decorator to handle transactions
def transactional(func):
    def wrapper(*args, **kwargs):
        connection = args[0] 
        try:
            result = func(*args, **kwargs)
            connection.commit()
            return result
        except Exception as e:
            connection.rollback()
            raise e
    return wrapper

# Decorator to retry a function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    print(f"Attempt {attempt}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed.")
                        raise
        return wrapper
    return decorator

# Database operation to fetch a user
@with_db_connection
@transactional
@retry_on_failure(retries=3, delay=2)  # Retry if an exception occurs
def get_user_by_id(conn, user_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()

# Database operation to update a user's email
@with_db_connection
@transactional
@retry_on_failure(retries=3, delay=2)  # Retry if an exception occurs
def update_user_email(conn, user_id, new_email):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE user_data SET email = %s WHERE user_id = %s", (new_email, user_id))
        return cursor.rowcount
    finally:
        cursor.close()

if __name__ == "__main__":
    # Test with a user ID
    try:
        update_user_email("00181703-f02e-4a65-9aa8-444b99d5ed17", "abdiesu@gmail.com")
        user = get_user_by_id("00181703-f02e-4a65-9aa8-444b99d5ed17")
        print(user)
    except Exception as e:
        print(f"Operation failed: {e}")
