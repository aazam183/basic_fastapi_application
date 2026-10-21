from sqlalchemy.orm import Session
from fastapi import HTTPException,status, Request, BackgroundTasks
from src.user.user_dtos import UserSchema, LoginSchema
from src.user.userModel import UserModel
from pwdlib import PasswordHash
import jwt
from jwt import InvalidTokenError
from src.utils.settings import settings
from datetime import datetime, timedelta
from src.utils.mail import sendMail



hash_password = PasswordHash.recommended()

def get_password_hash(password):
    return hash_password.hash(password)

def verify_password(plain_password, hashed_password):
    return hash_password.verify(plain_password, hashed_password)



async def registerUser(body:UserSchema, db:Session, bgTask: BackgroundTasks):

    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if user:
        raise HTTPException(400, detail="Username already exists...")

    if email:
        raise HTTPException(400,detail="email already exists...")

    # Hashing the password
    hash_password = get_password_hash(body.password)

    # body = body.model_dump()
    newUser = UserModel(
        name = body.name,
        username = body.username,
        hash_password = hash_password,
        email = body.email,
        phone = body.phone
        )
    


    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    ### SEND MAIL
    # res = await sendMail([newUser.email])
    bgTask.add_task(sendMail, [newUser.email])

    return newUser


def fetchUsers(db:Session):
    users = db.query(UserModel).all()
    return users


def fetchOne(id : int,db:Session):
    user = db.query(UserModel).get(id)
    if not user:
        raise HTTPException(404,detail="user not found...")
    return user

def loginUser(body:LoginSchema,db:Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="username is wrong ")
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you've enetered wrong password")
    # expire = datetime.now() + timedelta(seconds=20)
    expire = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"_id":user.id,"username":user.username,"exp":expire.timestamp()},settings.SECRET_KEY,settings.ALGORITHM)

    return{
        "token":token
    }

# TOKEN AUTHENTICATION

def authorization(req:Request,db:Session):
    try:
        token = req.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized request...")
        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.SECRET_KEY,settings.ALGORITHM)
        userId = data.get("_id")

######## JWT DECODE WILL AUTOMATICALLY RAISE AN ERROR IF THE TOKEN IS ALREADY EXPIREd BY THE DEFINED LOGIC ########
        
        user = db.query(UserModel).filter(UserModel.id == userId).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user ")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user ")
