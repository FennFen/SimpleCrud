from abc import ABC, abstractmethod
from typing import List

from app.core.record.domain.entity import Record


class RecordRepository(ABC):

    @abstractmethod
    def get(self, record_id: int) -> Record:
        raise NotImplementedError

    @abstractmethod
    def get_records(self, limit: int = 100, skip: int = 0) -> List[Record]:
        raise NotImplementedError

    @abstractmethod
    def add(self, record) -> Record:
        raise NotImplementedError

    @abstractmethod
    def update(self, record) -> Record:
        raise NotImplementedError

    @abstractmethod
    def delete(self, record_id: int) -> Record:
        raise NotImplementedError
