from pydantic import BaseModel

class taskSchema(BaseModel):
    title : str
    desc : str
    isCompleted : bool = False

class taskResponseSchema(BaseModel):
    id : int
    title : str
    desc : str
    isCompleted : bool = False
    user_id : int | None = 0

class taskUpdateSchema(BaseModel):
    title :str | None =  None
    desc : str | None = None
    isCompleted : bool | None = None