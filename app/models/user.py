from typing import Optional, Any, Union
from pydantic import BaseModel, Extra, Field

from app.models.automation import ItemBase as AutoItemBase
from app.models.rwmodel import RWModel
from app.models.dbmodel import DateTimeModelMixin, DBModelMixin, PyObjectId


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str