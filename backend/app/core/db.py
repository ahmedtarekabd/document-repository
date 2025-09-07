# Source from official FastAPI template:
# https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/db.py

from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.core.config import settings


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28

# Source: https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sqlmode#create-the-tables
def create_db_and_tables():
    from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)

# TODO: Used to initialize the database with some default data (Example: Seeding)
def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables uncommenting the next line
    # after importing all modules that define models in main.py
    create_db_and_tables()
    pass


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
