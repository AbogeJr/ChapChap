from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://aboge:root@localhost/chapchap", echo=True)

Base = declarative_base()

Session = sessionmaker()
