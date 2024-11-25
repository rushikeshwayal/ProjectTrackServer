import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask SQLAlchemy instance
db = SQLAlchemy()

# Define the SQLAlchemy engine using environment variables


connection_string = os.getenv('connection_string')
engine = create_engine(connection_string)

# Create a sessionmaker instance for direct access
SessionLocal = sessionmaker(bind=engine)

# Base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(50))
    access = Column(String(50))  # Corrected column name

user1 = User(username='user',email='user@gmail.com',password='userPassword',access='Investigator')
user2 = User(username='admin',email='admin@gmail.com',password='adminPassword',access='Admin')

session = SessionLocal()
try:
    # Add users to session
    session.add(user1)
    session.add(user2)
    
    session.commit()   # Commit the transactions

    print("Users added successfully!")
except Exception as e:
    session.rollback()
    print("Error adding users:", e)
finally:
    session.close()




# Initialize database and create tables
def init_db():
    Base.metadata.create_all(engine)

