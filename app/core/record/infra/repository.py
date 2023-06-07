from typing import List

from sqlalchemy.orm import Session

from app.core.record.domain.entity import Record
from app.core.record.domain.repository import RecordRepository
from app.core.record.infra.mapper import RecordMapper
from app.core.record.infra.model import Record as RecordDb

# TODO: atomicity on use case layer
class RecordDataRepository(RecordRepository):
    record_mapper = RecordMapper()

    def __init__(self, db: Session):
        self.__db = db

    def get(self, record_id: int) -> Record:
        db_item = self.__db.query(RecordDb).filter(RecordDb.id == record_id).first()
        return self.record_mapper.to_entity(db_item)

    def get_records(self, limit: int = 100, skip: int = 0) -> List[Record]:
        db_items = self.__db.query(RecordDb).offset(skip).limit(limit).all()
        return [self.record_mapper.to_entity(db_item) for db_item in db_items]

    def add(self, record: Record) -> Record:
        db_item = self.record_mapper.to_record(record)
        self.__db.add(db_item)
        self.__db.commit()
        self.__db.refresh(db_item)
        return self.record_mapper.to_entity(db_item)

    def update(self, record: Record) -> Record:
        self.__db.query(RecordDb).filter(RecordDb.id == record.id).update(
            {
                "title": record.title,
                "url": record.img_url
            }
        )
        self.__db.commit()
        db_item = self.__db.get(RecordDb, record.id)
        return self.record_mapper.to_entity(db_item)

    def delete(self, record_id: int) -> Record:
        db_item = self.__db.query(RecordDb).filter(RecordDb.id == record_id).first()
        self.__db.delete(db_item)
        self.__db.commit()
        return self.record_mapper.to_entity(db_item)


