from typing import List, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.dependencies import get_record_repository
from app.core.record.domain.entity import Record
from app.core.record.domain.repository import RecordRepository
from app.core.record.domain.value_objects import URL


class RecordBaseModel(BaseModel):
    title: str = Field(title="Record Title", min_length=1,
                       example="The Dark Side of the Moon", max_length=Record.MAX_TITLE_LENGTH)
    img: str = Field(title="Record Image URL", regex=URL.url_pattern,
                     example="https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png")

class RecordModel(RecordBaseModel):
    id: int = Field(title="Record ID", example=1, ge=1)

def to_model(record: Record) -> RecordModel:
    return RecordModel(id=record.id, title=record.title, img=record.img_url)


router = APIRouter()


@router.get("/", response_model=List[RecordModel])
def read_items(
    repo: RecordRepository = Depends(get_record_repository),
    skip: int = 0,
    limit: int = 100) -> Any:
    """
    Retrieve items.
    """
    items = repo.get_records(skip=skip, limit=limit)
    return [to_model(item) for item in items]

@router.get("/{record_id}", response_model=RecordModel)
def read_item(
    record_id: int,
    repo: RecordRepository = Depends(get_record_repository)) -> Any:
    """
    Retrieve item.
    """
    item = repo.get(record_id)
    return to_model(item)

@router.post("/", response_model=RecordModel)
def create_item(
    record_model: RecordBaseModel,
    repo: RecordRepository = Depends(get_record_repository)) -> Any:
    """
    Create item.
    """
    record = Record(title=record_model.title, img_url=record_model.img, record_id=None)
    item = repo.add(record)
    return to_model(item)

@router.put("/{record_id}", response_model=RecordModel)
def update_item(
    record_id: int,
    record_model: RecordBaseModel,
    repo: RecordRepository = Depends(get_record_repository)) -> Any:
    """
    Update item.
    """
    record = Record(title=record_model.title, img_url=record_model.img, record_id=record_id)
    item = repo.update(record)
    return to_model(item)


@router.delete("/{record_id}", response_model=RecordModel)
def delete_item(
    record_id: int,
    repo: RecordRepository = Depends(get_record_repository)) -> Any:
    """
    Delete item.
    """
    item = repo.delete(record_id)
    return to_model(item)
