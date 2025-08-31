from sqlalchemy import create_engine 
import os
from dotenv import load_dotenv

load_dotenv()
user_name = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database_name = os.getenv('POSTGRES_DB')
hostname = os.getenv('POSTGRES_HOST')
engine = create_engine(f'postgresql+psycopg2://{user_name}:{password}@{hostname}/{database_name}')

print("Connection Established Successfully !")