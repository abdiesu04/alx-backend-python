from seed import Seed

def stream_users_in_batches(batch_size):
    connection = Seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
        cursor.close()
        connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        # Process the filtered users
        for user in filtered_users:
            print(user)
            return user

# Example usage:
batch_processing(10)