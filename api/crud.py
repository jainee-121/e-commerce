from sqlalchemy.orm import Session
from . import models,schemas

def get_users(db:Session,user_id:int):
    return db.query(models.User).filter(models.User.id==user_id).first()

def get_user_by_email(db:Session,user_email:str):
    return db.query(models.User).filter(models.User.email== user_email).first()

def get_user(db:Session,skip:int=0,limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session,user:schemas.UserCreate):
    db_user=models.User(email=user.email,name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_products(db:Session,skip:int=0,limit:int=100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product_for_user(db:Session,user_id : int,category_id:int,product:schemas.ProductCreate):
    db_product=models.Product(**product.model_dump(),user_id=user_id,category_id=category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

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
