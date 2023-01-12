from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc://192.168.1.103/graphAPI?trusted_connection=yes&driver=SQL+Server+Native+Client+11.0'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()