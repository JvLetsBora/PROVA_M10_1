import asyncpg


class Migratinios():
    def __init__(self) -> None:
        self.async_pool = None

    async def create_pool(self):
        pool = await asyncpg.create_pool(
        user='username',
        password='password',
        database='postgres',
        host='postgres',
        port='5432'
        )
        return pool

    async def make_migrations(self):
        self.async_pool = await self.create_pool()
        try:
            async with self.async_pool.acquire() as connection:
                query = "CREATE TABLE pedidos ( id SERIAL PRIMARY KEY, descrition VARCHAR(255), name VARCHAR(255), email VARCHAR(255));"
                response = await connection.execute(query)
                return response
        except Exception as e:
            print(f"Erro ao criar as tabelas: {e}")
            return None
        


