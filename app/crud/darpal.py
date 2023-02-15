
from app.models.darpal import ItemInDB, ItemBase
from app.core.config import database_name, darpal_collection
from app.crud.base import CRUDBase


class CRUDDarpal(CRUDBase[ItemBase, ItemBase, ItemInDB]):
    pass


darpal_crud = CRUDDarpal(
    model=ItemInDB,
    database_name=database_name,
    collection_name=darpal_collection
)
