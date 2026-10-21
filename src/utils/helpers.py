from fastapi import Request, status, HTTPException, Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
from src.user.userModel import UserModel
from src.utils.db import getDB
import jwt
from jwt.exceptions import InvalidTokenError


# TOKEN AUTHENTICATION

def authorization(req:Request,db:Session = Depends(getDB)):
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


