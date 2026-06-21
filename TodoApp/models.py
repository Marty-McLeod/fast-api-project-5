from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# Defines user authentication data table schema
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)

# Defines a database table of parent class via Base
class Todos(Base):
    __tablename__ = "todos"
    
    # Create the columns based on data types and defined starting
    # parameters
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))