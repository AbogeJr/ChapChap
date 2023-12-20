from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_username = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}", echo=True
)

Base = declarative_base()

Session = sessionmaker()
