from fastapi import FastAPI
from src.utils.db import engine, Base
from src.tasks.taskRouter import task_routes
from src.user.userRouter import user_routes

Base.metadata.create_all(engine)


app = FastAPI(title="Task Manager App")
app.include_router(task_routes)
app.include_router(user_routes)