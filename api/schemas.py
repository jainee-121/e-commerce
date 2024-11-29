from pydantic import BaseModel


class TodoBase(BaseModel):
    title:str
    description:str|None=None

class TodoCreate(BaseModel):
    pass

class Todo(TodoBase):
    id:int 
    owner_id:int

    class config:
        orm_node=True

class UserBase(BaseModel):
    email:str
    name:str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id:int
    is_active:bool
    todos:list[Todo]=[]

    class config:
        orm_model=True

