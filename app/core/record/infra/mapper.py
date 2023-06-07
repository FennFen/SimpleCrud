from app.core.record.domain.entity import Record
from app.core.record.infra.model import Record as RecordDb


class RecordMapper:
    @staticmethod
    def to_entity(record: RecordDb) -> Record:
        return Record(
            record_id=record.id,
            title=record.title,
            img_url=record.url
        )
    
    @staticmethod
    def to_record(record: Record) -> RecordDb:
        record_db = RecordDb()
        record_db.id = record.id
        record_db.title = record.title
        record_db.url = record.img_url
        return record_db