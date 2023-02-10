
from app.models.controllers import ItemInDB, ItemBase
from app.core.config import database_name, controller_collection
from app.crud.base import CRUDBase


class CRUDControllers(CRUDBase[ItemBase, ItemBase, ItemInDB]):
    pass


controllers_crud = CRUDControllers(
    model=ItemInDB,
    database_name=database_name,
    collection_name=controller_collection
)
