from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import DATABASE_URL


engine = create_engine(DATABASE_URL)

BaseModel = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


def create_tables(engine: Engine = engine) -> None:
    """recreates tables"""
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables(engine)
