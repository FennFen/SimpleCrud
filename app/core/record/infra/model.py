from sqlalchemy import Column, Integer, String, Text

from app.core.record.domain.entity import Record as RecordEntity
from app.sql_infra.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(RecordEntity.MAX_TITLE_LENGTH))
    url = Column(Text)
