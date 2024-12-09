import aiosqlite
import asyncio

DATABASE = 'example.db'

async def async_fetch_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", users)
    print("Users older than 40:", older_users)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())