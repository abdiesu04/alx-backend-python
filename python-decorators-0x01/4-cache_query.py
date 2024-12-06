from seed import Seed

# Global query cache
query_cache = {}

# Decorator for managing database connections
def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = Seed.connect_to_prodev()
        try:
            return func(connection, *args, **kwargs)
        finally:
            connection.close()
    return wrapper

# Decorator for caching query results
def cache_query(func):
    def wrapper(*args, **kwargs):
        # Create a unique key for the cache based on function name, args, and kwargs
        cache_key = (func.__name__, args, frozenset(kwargs.items()))
        if cache_key in query_cache:
            print("Cache hit!")
            return query_cache[cache_key]
        print("Cache miss!")
        result = func(*args, **kwargs)
        query_cache[cache_key] = result
        return result
    return wrapper

@cache_query
@with_db_connection
def get_user_by_id(conn, user_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()

if __name__ == "__main__":
    # First call: Cache miss
    user = get_user_by_id(user_id="00181703-f02e-4a65-9aa8-444b99d5ed17")
    print(user)

    # Second call: Cache hit
    user = get_user_by_id(user_id="00181703-f02e-4a65-9aa8-444b99d5ed17")
    print(user)
    print(query_cache)