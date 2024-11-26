import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('connection_string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
