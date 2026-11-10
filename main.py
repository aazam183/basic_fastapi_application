from fastapi import FastAPI
from src.utils.db import engine, Base
from src.tasks.taskRouter import task_routes
from src.user.userRouter import user_routes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)


app = FastAPI(title="Task Manager App")
app.include_router(task_routes)
app.include_router(user_routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # add your deployed frontend URL here too
    allow_methods=["*"],
    allow_headers=["*"],
)