from pydantic import BaseModel


class CategoryBase(BaseModel):
    name:str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id:int

    class config:
        orm_node=True


class ProductBase(BaseModel):
    title:str
    description:str|None=None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id:int 
    user_id:int
    category_id:int
    
    class config:
        orm_node=True


class UserBase(BaseModel):
    email:str
    name:str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id:int
    is_active:bool

    class config:
        orm_model=True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str 




