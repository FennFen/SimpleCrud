from app.core.record.domain.value_objects import LimitedString, URL, RecordId


class Record:
    MAX_TITLE_LENGTH = 100
    __id: RecordId | None
    __title: LimitedString
    __img_url: URL

    def __init__(self, title: str, img_url: str, record_id: int = None):
        self.__id = RecordId(record_id) if record_id is not None else None
        self.__title = LimitedString(title, self.MAX_TITLE_LENGTH)
        self.__img_url = URL(img_url)

    @property
    def id(self) -> int | None:
        return self.__id if self.__id is not None else None

    @property
    def title(self) -> str:
        return self.__title

    @property
    def img_url(self) -> str:
        return self.__img_url
