import uvicorn
from fastapi import FastAPI

from .api import heros
from .db import create_db_and_tables

app = FastAPI(title="PoC of SQLModel with Alembic and Migration", docs_url="/")

# Include FastAPI api routers
app.include_router(heros.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def run_app() -> None:
    uvicorn.run(app=app)
