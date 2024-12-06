from seed import Seed

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = Seed.connect_to_prodev()
        try:
            return func(connection, *args, **kwargs)
        finally:
            connection.close()
    return wrapper


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
    

@with_db_connection
@transactional
def get_user_by_id(conn, user_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close() 

@with_db_connection
@transactional
def update_user_email(conn , user_id , new_email):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE user_data SET email = %s WHERE user_id = %s", (new_email, user_id))
        return cursor.rowcount
    finally:
        cursor.close()

if __name__ == "__main__":
    update_user_email("00181703-f02e-4a65-9aa8-444b99d5ed17", "abdiesu@gmail.com")
    user = get_user_by_id("00181703-f02e-4a65-9aa8-444b99d5ed17")
    
    print(user)
