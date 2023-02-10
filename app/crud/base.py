from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from bson import ObjectId
from app.core.config import MONGO_INITDB_DATABASE


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DBSchemaType = TypeVar("DBSchemaType", bound=BaseModel)

# TODO: Any -> concrete Type


class CRUDBase(Generic[CreateSchemaType, UpdateSchemaType, DBSchemaType]):
    def __init__(
        self,
        model: Type[DBSchemaType],
        collection_name: str,
        database_name: str = MONGO_INITDB_DATABASE
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A Pydantic model (schema) class
        * `collection_name`: A MongoDB collection name
        * `database_name`: A MongoDB database name
        """
        self.model = model
        self.database_name = database_name
        self.collection_name = collection_name

    async def read(
        self,
        db: Any,
        filter: object = None,
    ) -> Optional[DBSchemaType]:

        coll = db[self.database_name][self.collection_name]
        document = await coll.find_one(filter)
        if document:
            return self.model(**document)

    async def read_multi(
        self,
        db: Any,
        *,
        filter: object = None,
        sort: Any = ('_id'),
        skip: int = 0,
        limit: int = 100
    ) -> List[DBSchemaType]:

        coll = db[self.database_name][self.collection_name]
        documents = []
        cursor = coll.find(filter)
        cursor.sort(sort).skip(skip).limit(limit)

        async for document in cursor:
            documents.append(
                self.model(**document)
            )

        return documents

    async def create(
        self,
        db: Any,
        *,
        doc_in: CreateSchemaType
    ) -> DBSchemaType:

        coll = db[self.database_name][self.collection_name]
        doc_in_data = jsonable_encoder(doc_in)
        now = datetime.datetime.now()
        db_obj = self.model(
            **doc_in_data,
            createdAt=now,
            updatedAt=now
        )  # type: ignore
        # if isinstance(doc_in, dict):...
        db_obj = await coll.insert_one(db_obj.dict())
        db_doc_inserted = await coll.find_one({"_id": db_obj.inserted_id})

        return self.model(**db_doc_inserted)

    async def update(
        self,
        db: Any,
        *,
        db_doc_id: str,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[DBSchemaType]:

        coll = db[self.database_name][self.collection_name]
        db_doc = await coll.find_one({"_id": ObjectId(db_doc_id)})
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if db_doc:
            updated_db_doc = await coll.update_one(
                {"_id": ObjectId(db_doc_id)}, {"$set": update_data}
            )
            if updated_db_doc:
                db_doc_updated = await coll.find_one({'_id': ObjectId(db_doc_id)})
                return self.model(**db_doc_updated)
            else:
                return None

    async def delete(
        self,
        db: Any,
        *,
        db_doc_id: str
    ):

        coll = db[self.database_name][self.collection_name]
        db_doc = await coll.find_one({"_id": ObjectId(db_doc_id)})
        result = await coll.delete_one({'_id': ObjectId(db_doc_id)})

        return db_doc
