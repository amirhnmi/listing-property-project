from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqlconnector://***:***@127.0.0.1:3306/***")
sessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

