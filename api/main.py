from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import crud, models, schemas, auth
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# User Routes
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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


# Product Routes
@app.post("/users/{user_id}/products/", response_model=schemas.Product)
def create_product_for_user(category_id: int, product: schemas.ProductCreate,db: Session = Depends(get_db),current_user: schemas.User = Depends(auth.require_role("admin"))):
    db_cat=crud.get_single_category(db,category_id=category_id)
    if not (db_cat):
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.create_product_for_user(db, user_id=current_user.id,category_id=category_id, product=product)

@app.get("/products/", response_model=list[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


# Category Route
@app.post("/categories/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category_for_product(category: schemas.CategoryCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(auth.require_role("admin"))):
    return crud.create_category(db=db,category=category)

@app.get("/categories/", response_model=list[schemas.Category])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_category(db, skip=skip, limit=limit)
    return categories

@app.get("/me/", response_model=schemas.User)
def get_current_user_info(
    current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user