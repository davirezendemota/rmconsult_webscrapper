from typing import TypeVar

from core.BaseModel import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


def update_model(model: TModel, data: dict) -> TModel:
    for key, value in data.items():
        setattr(model, key, value)
    return model
