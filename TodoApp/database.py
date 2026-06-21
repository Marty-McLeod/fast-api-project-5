from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# PostgreSQL & MySQL passwords: RiddleSticks16!
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:RiddleSticks16!@localhost/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:RiddleSticks16!@127.0.0.1:3306/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create an object of the database for creating & interacting with the DB
Base = declarative_base()
