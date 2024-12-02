from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

owner_products=Table(
    "owner_products",
    Base.metadata,
    Column('user_id',Integer,ForeignKey("users.id"),primary_key=True),
    Column("product_id",Integer,ForeignKey("product.id"),primary_key=True),)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)
    product = relationship("products",secondary=owner_products,back_populates="owner")
    is_active = Column(Boolean,default=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User",secondary=owner_products,back_populates="products")

