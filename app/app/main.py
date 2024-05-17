import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from config.db import Migratinios
from models import pedidos

migrations = Migratinios()


app = FastAPI(docs_url="/api/docs")


@app.post("/migratinios")
async def root():
    response = await migrations.make_migrations()
    return {"Resposta": response}

@app.post("/pedido/novo")
async def create_pedido_for_user(
    pedido: pedidos.PedidoCreate
):
    return await pedidos.create_pedido(pedido=pedido)

@app.get("/pedido/pedidos/{id}")
async def create_pedido_for_user(
    id: int
):
    return await pedidos.get_pedido_id(id=id)


@app.get("/pedido/pedidos")
async def tasks():
    tasks = await pedidos.get_pedidos()
    return tasks

@app.delete("/pedido/pedidos/{id}")
async def create_pedido_for_user(
    id: int
):
    return await pedidos.delete_pedido(id=id)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)