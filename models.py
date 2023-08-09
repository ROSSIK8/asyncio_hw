from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Integer, String, Column
import os
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


DB_DSN = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(DB_DSN)
Base = declarative_base()

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class SwapiPeople(Base):

    __tablename__ = 'swapi_people'
    id = Column(Integer, primary_key=True)
    detail = Column(String, nullable=True)
    birth_year = Column(String, nullable=True)
    eye_color = Column(String, nullable=True)
    films = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    hair_color = Column(String, nullable=True)
    height = Column(String, nullable=True)
    homeworld = Column(String, nullable=True)
    mass = Column(String, nullable=True)
    name = Column(String, nullable=True)
    skin_color = Column(String, nullable=True)
    species = Column(String, nullable=True)
    starships = Column(String, nullable=True)
    vehicles = Column(String, nullable=True)


# class SwapiPeople(Base):
#     __tablename__ = 'swapi_people'
#     id = Column(Integer, primary_key=True)
#     detail = Column(String, nullable=True)
#     birth_year = Column(String, nullable=True)
#     eye_color = Column(String, nullable=True)
#     films = Column(String, nullable=True)
#     gender = Column(String, nullable=True)
#     hair_color = Column(String, nullable=True)
#     height = Column(String, nullable=True)
#     homeworld = Column(String, nullable=True)
#     mass = Column(String, nullable=True)
#     name = Column(String, nullable=True)
#     skin_color = Column(String, nullable=True)
#     species = Column(String, nullable=True)
#     starships = Column(String, nullable=True)
#     vehicles = Column(String, nullable=True)
#
#     created = Column(String, nullable=True)
#     edited = Column(String, nullable=True)
#     url = Column(String, nullable=True)
