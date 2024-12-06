from seed import Seed

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = Seed.connect_to_prodev()
        try:
            return func(connection, *args, **kwargs)  
        finally:
            connection.close()  
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close() 

if __name__ == "__main__":
    user = get_user_by_id(user_id="00181703-f02e-4a65-9aa8-444b99d5ed17") 
    print(user)
