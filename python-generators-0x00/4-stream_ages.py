import mysql
from seed import Seed
def stream_user_ages():
    connection = Seed.connect_to_prodev()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT age FROM user_data
        """)
        for row in cursor:
            yield row['age']
    except mysql.connector.Error as err:
        print(f"Error fetching user ages: {err}")
        return
    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    total = 0
    i = 0
    for age in stream_user_ages():
        total += age   
        i += 1 
    print(f"Average age: {total / i}")
