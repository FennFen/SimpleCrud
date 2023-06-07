from fastapi import Depends

from app.core.record.domain.repository import RecordRepository
from app.sql_infra.database import SessionLocal


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_record_repository(db=Depends(get_db)) -> RecordRepository:
    from app.core.record.infra.repository import RecordDataRepository
    return RecordDataRepository(db)