from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine

from fastapi_app.models.hero import (  # Import your models
    Hero,
    HeroCreate,
    HeroRead,
    HeroUpdate,
)

# Setup in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)


# Create the database schema
def create_test_schema():
    SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="module")
def session():
    create_test_schema()
    with Session(engine) as session:
        yield session


def test_default_values(session: Session):
    # Create a Hero instance without specifying created_at and updated_at
    hero = Hero(name="Superman", secret_name="Clark Kent")
    session.add(hero)
    session.commit()
    session.refresh(hero)

    assert hero.created_at is not None
    assert hero.updated_at is not None
    assert isinstance(hero.created_at, datetime)
    assert isinstance(hero.updated_at, datetime)


def test_hero_create_model():
    hero_create = HeroCreate(name="Batman", secret_name="Bruce Wayne")
    assert hero_create.name == "Batman"
    assert hero_create.secret_name == "Bruce Wayne"
    assert hero_create.age is None
    assert hero_create.power is None
    # assert hero_create.created_at is None
    # assert hero_create.updated_at is None


def test_hero_read_model(session: Session):
    # Add a Hero to the database
    hero = Hero(name="Wonder Woman", secret_name="Diana Prince")
    session.add(hero)
    session.commit()
    session.refresh(hero)

    # Test HeroRead model
    hero_read = HeroRead.model_validate(hero)
    assert hero_read.id == hero.id
    assert hero_read.name == "Wonder Woman"
    assert hero_read.secret_name == "Diana Prince"
    assert hero_read.age is None
    assert hero_read.power is None
    assert hero_read.created_at == hero.created_at
    assert hero_read.updated_at == hero.updated_at


def test_hero_update_model():
    # Create an instance of HeroUpdate
    hero_update = HeroUpdate(name="Aquaman", secret_name="Arthur Curry", age=30)
    assert hero_update.name == "Aquaman"
    assert hero_update.secret_name == "Arthur Curry"
    assert hero_update.age == 30
