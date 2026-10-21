from fastapi import APIRouter, Depends,status
from src.tasks import taskController
from src.tasks.task_dtos import taskSchema, taskUpdateSchema, taskResponseSchema
from src.utils.db import getDB
from src.utils.helpers import authorization
from src.user.userModel import UserModel
from typing import List
from sqlalchemy.orm import Session


task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create", response_model=taskResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task(body:taskSchema, db : Session = Depends(getDB), user:UserModel = Depends(authorization)):
    print(user)
    return taskController.create_task(body,db,user)

@task_routes.get("/fetchAll", response_model=List[taskResponseSchema], status_code=status.HTTP_200_OK)
def get_tasks(db:Session = Depends(getDB), user:UserModel = Depends(authorization)):
    return taskController.get_allTasks(db, user)

@task_routes.get("/fetch/{taskId}",response_model=taskResponseSchema, status_code=status.HTTP_200_OK)
def getTaskByID(taskId:int,db:Session = Depends(getDB), user:UserModel = Depends(authorization)):
    return taskController.getTaskByID(taskId,db)

@task_routes.put("/update/{taskId}",response_model=taskResponseSchema, status_code=status.HTTP_201_CREATED)
def updateTask(body:taskUpdateSchema, taskId:int, db:Session=Depends(getDB), user:UserModel = Depends(authorization)):
    return taskController.updateTask(body,taskId,db,user)

@task_routes.delete("/delete/{taskId}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def deleteTask(taskId:int,db:Session=Depends(getDB), user : UserModel = Depends(authorization)):
    return taskController.deleteTask(taskId,db,user)