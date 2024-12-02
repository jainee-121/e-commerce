from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Routes
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_user(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}/", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_users(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/products/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product_for_user(user_id: int,category_id:int,product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_user = crud.get_users(db, user_id=user_id)
    db_cat=crud.get_single_category(db,category_id=category_id)
    if not (db_user and db_cat):
        raise HTTPException(status_code=404, detail="User or Category not found")
    return crud.create_product_for_user(db, user_id=user_id,category_id=category_id, product=product)

@app.get("/products/", response_model=list[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.post("/categories/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category_for_product(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db,category=category)

@app.get("/categories/", response_model=list[schemas.Category])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_category(db, skip=skip, limit=limit)
    return categories
