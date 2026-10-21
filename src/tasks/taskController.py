from src.tasks.task_dtos import taskSchema, taskUpdateSchema
from sqlalchemy.orm import Session
from src.tasks.taskModel import taskModel
from fastapi import HTTPException
from src.user.userModel import UserModel



def create_task(body:taskSchema, db:Session, user: UserModel):
    data = body.model_dump()
    new_task = taskModel(title = data["title"],
                         desc = data["desc"],
                         isCompleted = data["isCompleted"],
                         user_id = user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
            


def get_allTasks(db:Session, user: UserModel):
    tasks = db.query(taskModel).filter(taskModel.user_id == user.id)
    return tasks

    

def getTaskByID(taskID : int,db:Session):
    task = db.query(taskModel).get(taskID)
    if not task:
        raise HTTPException(404,detail="ID not found")

    return task
    

def updateTask (body:taskUpdateSchema,taskID:int,db:Session, user:UserModel):
    task : taskModel = db.query(taskModel).get(taskID)
    if not task:
        raise HTTPException(404, detail="id not found")

    if task.user_id != user.id:
        raise HTTPException(401, detail="Unauthorized request....")

    
    body = body.model_dump(exclude_unset=True)
    for key, value in body.items():
        setattr(task,key,value)
    # task.title = body.title
    # task.desc = body.desc
    # task.isCompleted = body.isCompleted
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def deleteTask(taskId:int, db:Session, user: UserModel):
    task = db.query(taskModel).get(taskId)
    if not task:
        raise HTTPException(404,detail="invalid task id")
    if task.user_id != user.id:
        raise HTTPException(401, detail="Unauthorized request....")
    db.delete(task)
    db.commit()
    return None