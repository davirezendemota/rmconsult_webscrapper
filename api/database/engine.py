from datetime import datetime, timezone

from sqlalchemy import event
from sqlalchemy.orm import ORMExecuteState, with_loader_criteria
from sqlmodel import Session, create_engine

from core.BaseModel import BaseModel
from core.config import env

__engine = create_engine(env.DATABASE_URL)

# SQLModel.metadata.create_all(engine)


def get_session():  # pragma: no cover
    with Session(__engine) as session:
        yield session
