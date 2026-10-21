from fastapi import APIRouter, Depends, Request,status, BackgroundTasks
from sqlalchemy.orm import Session
from src.user.user_dtos import UserSchema,ResponseSchema, LoginSchema
from src.utils.db import getDB
from src.user import userController
from typing import List



user_routes = APIRouter(prefix="/user")

@user_routes.post("/register",response_model=ResponseSchema,status_code=status.HTTP_201_CREATED)
async def registerUser(body: UserSchema, bgTask : BackgroundTasks ,db:Session = Depends(getDB)):
    return await userController.registerUser(body,db,bgTask)

@user_routes.get("/fetch",response_model=List[ResponseSchema] ,status_code=status.HTTP_200_OK)
def fetchUser(db:Session = Depends(getDB)):
    return userController.fetchUsers(db)

@user_routes.get("/fetchOne/{id}",response_model=ResponseSchema,status_code=status.HTTP_200_OK)
def fetchOne(id:int,db:Session = Depends(getDB)):
    return userController.fetchOne(id,db)

@user_routes.post("/login",status_code=status.HTTP_200_OK)
def loginUser(body:LoginSchema,db:Session = Depends(getDB)):
    return userController.loginUser(body,db)

@user_routes.get("/auth",status_code=status.HTTP_200_OK, response_model=ResponseSchema)
def auth(req: Request, db:Session=Depends(getDB)):
    return userController.authorization(req,db)