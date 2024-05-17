import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from config.db import Migratinios

init_migrations = Migratinios()


app = FastAPI(docs_url="/api/docs")


@app.post("/migratinios")
async def root():
    response = await init_migrations.make_migrations()
    return {"Resposta: ": response}

# @app.post("/users/{user_id}/tasks/")
# async def create_task_for_user(
#     user_id: int, task: schemas.TaskBase, db:  asyncpg.Pool = Depends(pool_session)
# ):
#     return await crud.create_user_task(db=db, task=task, user_id=user_id)

# @app.get("/tasks/")
# async def tasks(skip: int = 0, limit: int = 100, db: asyncpg.Pool = Depends(pool_session)):
#     tasks = await crud.get_tasks(db, skip=skip, limit=limit)
#     return tasks

# @app.delete("/tasks/{task_id}")
# async def delete_task(task_id: int, db: asyncpg.Pool = Depends(pool_session)):
#     return await crud.delete_task(db=db, task_id=task_id)

# @app.put("/tasks/{task_id}")
# async def update_task(task_id: int, task_update: schemas.TaskUpdate, db: asyncpg.Pool = Depends(pool_session)):
#     return await crud.update_task(db=db, task_id=task_id, task_data=task_update)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)