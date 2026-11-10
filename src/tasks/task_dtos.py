from pydantic import BaseModel
from datetime import datetime


class taskSchema(BaseModel):
    title : str
    desc : str
    isCompleted : bool = False

class taskResponseSchema(BaseModel):
    id : int
    title : str
    desc : str
    isCompleted : bool = False
    created_at: datetime | None = None
    user_id : int | None = 0

class taskUpdateSchema(BaseModel):
    title :str | None =  None
    desc : str | None = None
    isCompleted : bool | None = None