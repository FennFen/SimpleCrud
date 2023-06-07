import re


class RecordId(int):
    __min_value = 1

    class RecordMustBePositiveInteger(Exception):
        __error_message = 'Record id must be positive integer'

        def __init__(self):
            super().__init__(self.__error_message)

    def __new__(cls, value: int):
        if value < cls.__min_value:
            raise cls.RecordMustBePositiveInteger
        return super().__new__(cls, value)


class LimitedString(str):
    __max_length: int

    class StringValueIsTooLong(Exception):
        __error_message = 'String value is too long: {} > {}'

        def __init__(self, value: str, max_length: int):
            super().__init__(self.__error_message.format(len(value), max_length))

    def __new__(cls, value: str, max_length: int = 255):
        if len(value) > max_length:
            raise cls.StringValueIsTooLong(value, max_length)
        cls.__max_length = max_length
        return super().__new__(cls, value)


class URL(str):
    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$", re.IGNORECASE
    )

    class StringValueIsNotAValidURL(Exception):
        __error_message = 'String value is not a valid URL: {}'

        def __init__(self, value: str):
            super().__init__(self.__error_message.format(value))

    @staticmethod
    def __is_valid_url(url):
        return bool(URL.url_pattern.match(url))

    def __new__(cls, value: str):
        if not value or not cls.__is_valid_url(value):
            raise cls.StringValueIsNotAValidURL(value)
        return super().__new__(cls, value)
