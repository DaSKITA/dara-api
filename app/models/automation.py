from typing import Optional, Any, Union
from pydantic import BaseModel, Extra, Field

from app.models.rwmodel import RWModel
from app.models.dbmodel import DateTimeModelMixin, DBModelMixin, PyObjectId


class ItemBase(RWModel):
    format: str = Field(...)
    version: str = Field(...)
    definition: dict = Field(...)


class Item(DateTimeModelMixin, ItemBase):
    # Add optional created and updated timestamps
    pass


class ItemInDB(DBModelMixin, Item):
    # Add optional id information
    id: PyObjectId = Field(
        default_factory=PyObjectId,
        description='The id of a controller instance. The id is necessary to distinguish several processing tasks of the same data item (locally unique ID that can be based on the database implementation).',
        examples=['f1424f86-ca0f-4f0c-9438-43cc00509931'],
        title='_id',
        alias='_id'
    )
