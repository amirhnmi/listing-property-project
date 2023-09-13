from dependencies.database import Base
from sqlalchemy import Column,String,Integer,DateTime,Boolean,ForeignKey,Date
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    username = Column(String(length=250),unique=True ,nullable=False)
    fullname = Column(String(length=250), nullable=True)
    email = Column(String(length=250), nullable=False,unique=True)
    password = Column(String(length=500), nullable=False)
    dateOfBirth = Column(Date, nullable=True)
    gender = Column(String(length=50),nullable=True,default="NOT_SPECIFIED")
    token = Column(Integer, nullable=True)
    createAt = Column(DateTime,nullable=True)
    updateAt = Column(DateTime, nullable=True)
    listings = relationship("Listing", back_populates="users")


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    type = Column(String(length=50),nullable=False)
    availableNow = Column(Boolean, nullable=True,default=True)
    address = Column(String(length=500),nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="listings")
    createAt = Column(DateTime, nullable=True)
    updateAt = Column(DateTime, nullable=True)