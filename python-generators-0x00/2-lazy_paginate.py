import mysql.connector
from seed import Seed

connection = Seed.connect_to_prodev()

def paginate_users(page_size, offset):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM user_data LIMIT %s OFFSET %s
        """, (page_size, offset))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error as err:
        print(f"Error fetching paginated data: {err}")
        return []

def lazy_paginate(page_size):
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        for row in rows:
            yield row
        offset += page_size

if connection:
    try:
        for user in lazy_paginate(2):
            print(user)
    finally:
        connection.close()