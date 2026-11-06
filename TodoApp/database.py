from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db' #datbase will be inside of this direction on our fastpi app

#Engine to open up a conection and use db

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) #by default sqllite, each thread will independently handle one request to prevent any type of accident sharing of the same connection for different type of requests but fastpi can have more than one thread to communicate with sqlbasedatabase

#create an instance to became an actual db in the future
SessionLocal = sessionmaker(autocommit = False, autoflush=False,bind=engine) #bind to the engine and make sure that autocommits and autoflush are false so db doesnt do nothing automatically 

Base = declarative_base() #when we call database.py file be able to create a base which is an object of database to control the database (to create an object to interact with the tables we create on the future)
