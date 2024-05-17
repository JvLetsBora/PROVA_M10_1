from schemas import *
import asyncpg
from passlib.context import CryptContext

class db_config():
    def __init__(self) -> None:
        self.async_pool = None

    async def set_pool(self):
         self.async_pool = await self.create_pool()
        

    async def create_pool(self):
        pool = await asyncpg.create_pool(
            user='username',
            password='password',
            database='postgres',
            host='postgres',
            port='5432'
        )
        return pool

db = db_config()

async def pool_session():
    if db.async_pool == None:
        await db.set_pool()
    return db.async_pool


async def get_tasks(db: asyncpg.Pool, skip: int = 0, limit: int = 100):
    try:
        async with db.acquire() as connection:
            # Executa a consulta SQL diretamente
            query = f"SELECT * FROM tasks OFFSET {skip} LIMIT {limit}"
            rows = await connection.fetch(query)

            # Transforma as linhas em dicionários
            tasks = [dict(row) for row in rows]
            return tasks
    except Exception as e:
        print(f"Erro ao obter tasks: {e}")
        return None
    
async def create_user_task(db: asyncpg.Pool, task: TaskCreate, user_id: int):
    try:
        async with db.acquire() as connection:
        # Executa a consulta SQL diretamente
            query = f"""
                INSERT INTO tasks (user_id, title, description, is_active)
                VALUES ({user_id} ,'{task.title}', '{task.description}', false)
                RETURNING id;
                """
            rows = await connection.fetch(query)
            response = Task(
                id=int(rows[0]["id"]),
                description=task.description,
                is_active= False,
                user_id=user_id,
                title=task.title
            )
            return response
        
    except Exception as e:
        return {
            "msg": f"Erro ao criar tarefa: {str(e)}"
        }

async def delete_task(db: asyncpg.Pool, task_id: int) -> dict: 
    try:
        async with db.acquire() as connection:
        # Executa a consulta SQL diretamente
            query = f"DELETE FROM tasks WHERE id = {task_id};"
            rows = await connection.fetch(query)
            task = [dict(row) for row in rows]
            print(task)
            return {
                "msg": "Deletado com sucesso!"
            }
    except Exception as e:
        return {
            "msg": f"Erro ao excluir a tarefa: {str(e)}"
        }

async def update_task(db: asyncpg.Pool, task_id: int, task_data: TaskUpdate):
    try:
        async with db.acquire() as connection:
        # Executa a consulta SQL diretamente
            query = f"UPDATE tasks SET title = '{task_data.title}', description = '{task_data.description}' WHERE id = {task_id};"
            rows = await connection.fetch(query)
            return {
                "msg": "Atualizado com sucesso!"
            }
    except Exception as e:
        return {
            "msg": f"Erro ao atualizar a tarefa: {str(e)}"
        }
