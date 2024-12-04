from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, auth

# user
def get_users(db:Session,user_id:int):
    return db.query(models.User).filter(models.User.id==user_id).first()

def get_user_by_email(db:Session,user_email:str):
    user=db.query(models.User).filter(models.User.email== user_email).first()
    return user

def get_user(db:Session,skip:int=0,limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session,user:schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        role=user.role 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not auth.verify_password(password, user.hashed_password):
        return False
    return user

# product
def get_products(db:Session,skip:int=0,limit:int=100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_single_product(db:Session,product_id:int):
    return db.query(models.Product).filter(models.Product.id==product_id).first()

def create_product_for_user(db:Session,user_id : int,category_id:int,product:schemas.ProductCreate):
    db_product=models.Product(**product.model_dump(),user_id=user_id,category_id=category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_for_user(db:Session,user_id : int,category_id:int,product:schemas.ProductUpdate):
    # db_get_product=get_single_product(db,product_id=product_id)
    db_product=models.Product(**product.model_dump(),user_id=user_id,category_id=category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# category
def get_single_category(db:Session,category_id:int):
    return db.query(models.Category).filter(models.Category.id==category_id).first()

def get_category(db:Session,skip:int=0,limit:int=100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db:Session,category=schemas.CategoryCreate):
    db_category=models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category