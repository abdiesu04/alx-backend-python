from seed import Seed
import mysql.connector

def paginate_users(connection, page_size, offset):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, name, email, age
            FROM user_data
            LIMIT %s OFFSET %s
        """, (page_size, offset))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error as err:
        print(f"Error fetching paginated data: {err}")
        return []

def lazy_paginate(connection, page_size):
    offset = 0
    while True:
        rows = paginate_users(connection, page_size, offset)
        if not rows:
            break
        for row in rows:
            yield row
        offset += page_size

connection = Seed.connect_to_prodev()
if connection:
    for user in lazy_paginate(connection, 2):
        print(user)
connection.close()