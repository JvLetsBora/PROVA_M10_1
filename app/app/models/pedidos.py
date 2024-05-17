from models.schemas.pedido import *
import asyncpg

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


async def get_pedido_id(id:int):
    db = await pool_session()
    try:
        async with db.acquire() as connection:
            # Executa a consulta SQL diretamente
            query = f"SELECT * FROM pedidos WHERE id =  {id};"
            rows = await connection.fetch(query)

            # Transforma as linhas em dicionários
            pedidos = [dict(row) for row in rows]
            if pedidos[0] is None:
                return {
                    "Resposta":"Usuário {id} não encontrado"
                }

            return pedidos
    except Exception as e:
        print(f"Erro ao obter pedido: {e}")
        return {
            "Resposta":"Usuário {id} não encontrado"
        }

async def get_pedidos():
    db = await pool_session()
    try:
        async with db.acquire() as connection:
            # Executa a consulta SQL diretamente
            query = f"SELECT * FROM pedidos"
            rows = await connection.fetch(query)

            # Transforma as linhas em dicionários
            pedidos = [dict(row) for row in rows]
            return pedidos
    except Exception as e:
        print(f"Erro ao obter pedidos: {e}")
        return None
    
async def create_pedido(pedido: PedidoCreate) -> PedidoCreateResponse:
    db = await pool_session()
    try:
        async with db.acquire() as connection:
        # Executa a consulta SQL diretamente
            query = f"""
                INSERT INTO pedidos (descrition, name, email)
                VALUES ('{pedido.descrition}', '{pedido.name}', '{pedido.email}')
                RETURNING id;
                """
            rows = await connection.fetch(query)
            response = PedidoCreateResponse(
                id=int(rows[0]["id"]),
            )
            return response
        
    except Exception as e:
        return {
            "msg": f"Erro ao criar tarefa: {str(e)}"
        }

async def delete_pedido(id: int) -> dict: 
    db = await pool_session()
    pedido = await get_pedido_id(id)
    if pedido["Resposta"]:
        return {
            "Resposta": pedido["Resposta"]
        }

    try:
        async with db.acquire() as connection:
        # Executa a consulta SQL diretamente
            query = f"DELETE FROM pedidos WHERE id = {id};"
            rows = await connection.fetch(query)
            print(rows)
            pedido = [dict(row) for row in rows]
            return {
                "Resposta": "Deletado com sucesso!"
            }
    except Exception as e:
        return {
            "Resposta": f"Erro ao excluir o pedido: {str(e)}, usuário não encontrado."
        }

# async def update_task(db: asyncpg.Pool, task_id: int, task_data: TaskUpdate):
#     try:
#         async with db.acquire() as connection:
#         # Executa a consulta SQL diretamente
#             query = f"UPDATE tasks SET title = '{task_data.title}', description = '{task_data.description}' WHERE id = {task_id};"
#             rows = await connection.fetch(query)
#             return {
#                 "msg": "Atualizado com sucesso!"
#             }
#     except Exception as e:
#         return {
#             "msg": f"Erro ao atualizar a tarefa: {str(e)}"
#         }
