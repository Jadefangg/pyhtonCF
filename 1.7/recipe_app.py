#OBJECT REALTIONAL MAPPER - 1.7 
#SQLALCHEMY installed

from sqlalchemy import create_engine #importing the create_engine function from the sqlalchemy module

# Create a connection string using the existing credentials which connects to the task_database
connection_string = "mysql+mysqlconnector://cf-python:password@localhost/task_database" #this has my username(cf-python) and password(password) for the database(task_database)

# Create the engine
engine = create_engine(connection_string, echo=True)