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


connection_string = f"postgresql+psycopg2://default:m8fGg2pOqADn@ep-curly-wildflower-a42kf29p.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"
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


# Initialize database and create tables
def init_db():
    Base.metadata.create_all(engine)

