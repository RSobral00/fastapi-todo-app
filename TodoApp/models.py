#Way for sqlalchemy to be able to udnerstand what type of database tables we will be creating
#database model is the actual record of what is inside the database table 
#e.g. table todos inside of todo tables each will have id, title, description, priority and complete, will make sure that is an anctual record that we are able to use in our fastapi app

from .database import Base #database import
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    first_name = Column(String,unique=False)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    role = Column(String)
    phone_number = Column(String)


    
#create new table 'todos'
class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey("users.id"))


    