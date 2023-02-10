from typing import Optional, Any, Union
from pydantic import BaseModel, Extra, Field

from app.models.automation import ItemBase as AutoItemBase
from app.models.rwmodel import RWModel
from app.models.dbmodel import DateTimeModelMixin, DBModelMixin, PyObjectId



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
