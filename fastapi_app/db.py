import os
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = os.path.join(
    Path(__file__).parent.parent, "db", "local-database.db"
)
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
