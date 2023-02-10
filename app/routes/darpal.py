
from typing import List
from fastapi import APIRouter, Depends, Body, HTTPException
from app.models.darpal import *
from app.crud.darpal import darpal_crud
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.user import User
from app.routes.users import get_current_active_user

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/darpal",
    tags=["darpal"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "Success"}
    }
)


@router.get(
    '/',
    response_model=List[ItemInDB],
    response_model_exclude_none=True,
    summary="Retrieve all items",
    description="Retrieve all items"
)
async def get_item_multi(
    sort: Optional[Any] = ('_id'),
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database),
    filterQuery=None
):
    return await darpal_crud.read_multi(db=db, filter=filterQuery, sort=sort, skip=skip, limit=limit)


@router.get(
    '/{id}',
    response_model=ItemInDB,
    summary="Retrieve item",
    description="Retrieve item"
)
async def get_item(
    id: str,
    db: AsyncIOMotorClient = Depends(get_database)
) -> Any:
    return await darpal_crud.read(db=db, filter={"controllerId": controller_id})


@router.post(
    '/',
    response_model=ItemInDB,
    summary="Submit a new item or update an existing",
    description="Submit a new item"
)
async def post_item(
    current_user: User = Depends(get_current_active_user),
    item: ItemBase = Body(...),
    db: AsyncIOMotorClient = Depends(get_database),

) -> Any:
    # Check whether we have already a controller in db
    controller_from_db = await darpal_crud.read(db=db, filter={"controllerId": item.controllerId})
    if controller_from_db != None:
        # Update existing item in db
        controller_from_db = await darpal_crud.update(db=db, db_doc_id=str(controller_from_db.id), obj_in=item)

    else:
        # Create a new item and submit it to the db
        controller_from_db = await darpal_crud.create(db=db, doc_in=item)

    return controller_from_db


@router.delete(
    '/{controller_id}',
    response_model=ItemInDB,
    summary="Delete an item",
    description="Delete an item"
)
async def delete_item(
    controller_id: str,
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_active_user),
) -> Any:

    controller_from_db = await darpal_crud.read(db=db, filter={"controllerId": controller_id})

    if controller_from_db != None:
        return await darpal_crud.delete(db=db, db_doc_id=str(controller_from_db.id))
    else:
        raise HTTPException(status_code=404, detail="Controller not found")


"""
@router.get(
    '/{controller_id}/host',
    response_model=Dict,
    summary="Retrieve hosted id",
    description="Retrieve hosted id"
)
async def get_hosted_id(
    controller_id: str,
    db: AsyncIOMotorClient = Depends(get_database),
) -> Any:
    controller_entry = await darpal_crud.read(db=db, filter={"controller_id": controller_id})
    if controller_entry:
        return await retrieve_hosted_id(controller_entry=controller_entry)
    else:
        raise HTTPException(status_code=404, detail="Controller not found")
"""
