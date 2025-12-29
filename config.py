import os
from dotenv import load_dotenv

load_dotenv() # Load vars from .env

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # SQLAlchemy URI construction
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASS')
    host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')

    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
