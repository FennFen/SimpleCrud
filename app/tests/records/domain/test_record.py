from app.core.record.domain.entity import Record
from app.core.record.domain.value_objects import LimitedString, URL, RecordId

def assert_record(record: Record, record_id: int | None, title: str, img_url: str):
    assert record.id == record_id
    assert record.title == title
    assert record.img_url == img_url

def test_record_all_fields():
    """
    Test that Record entity can be instantiated with all fields.
    All the fields provided will be valid
    """
    valid_id = 1
    valid_title = "A title"
    valid_img_url = "https://example.com"

    record = Record(valid_title, valid_img_url, valid_id)

    assert_record(record, valid_id, valid_title, valid_img_url)

def test_record_minimum_fields():
    """
    Test that Record entity can be instantiated with the minimum fields.
    All the fields provided will be valid
    """
    valid_title = "A title"
    valid_img_url = "https://example.com"

    record = Record(valid_title, valid_img_url)

    assert_record(record, None, valid_title, valid_img_url)


def test_record_invalid_title():
    """
    Test that Record entity cannot be instantiated with an invalid title.
    """
    invalid_title = "A title" * 100
    valid_img_url = "https://example.com"

    try:
        Record(invalid_title, valid_img_url)
        assert False
    except LimitedString.StringValueIsTooLong:
        assert True


def test_record_invalid_img_url():
    """
    Test that Record entity cannot be instantiated with an invalid img_url.
    """
    valid_title = "A title"
    invalid_img_url = "example.com"

    try:
        Record(valid_title, invalid_img_url)
        assert False
    except URL.StringValueIsNotAValidURL:
        assert True

def test_record_invalid_id():
    """
    Test that Record entity cannot be instantiated with an invalid id.
    """
    invalid_id = 0
    valid_title = "A title"
    valid_img_url = "https://example.com"

    try:
        Record(valid_title, valid_img_url, invalid_id)
        assert False
    except RecordId.RecordMustBePositiveInteger:
        assert True
