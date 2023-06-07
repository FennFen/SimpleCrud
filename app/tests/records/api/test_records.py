from typing import Dict, Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app.core.record.infra.model import Record as RecordDb


def assert_record(received: Dict[str, Any], db: Session) -> None:
    record = db.query(RecordDb).filter(RecordDb.id == received["id"]).first()
    db.refresh(record)

    assert record is not None
    assert record.title == received["title"]
    assert record.url == received["img"]
    assert record.id == received["id"]

def create_record_in_db(db) -> RecordDb:
    db.query(RecordDb).delete()
    record_db = RecordDb()
    record_db.title = "title 1"
    record_db.url = "https://upload.wikimedia.org/wikipedia/en/3/3b/an_image.png"
    db.add(record_db)
    db.commit()
    db.refresh(record_db)
    return record_db

def test_create_record(
    client: TestClient, db: Session
) -> None:
    data = {
        "title": "The Dark Side of the Moon",
        "img": "https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png",
    }
    response = client.post(
        "/api/v1/records/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert_record(content, db)


def test_read_record(
    client: TestClient, db: Session
) -> None:
    record_db = create_record_in_db(db)

    response = client.get(
        f"/api/v1/records/{record_db.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert_record(content, db)

def test_read_records(
    client: TestClient, db: Session
) -> None:
    create_record_in_db(db)

    response = client.get(
        "/api/v1/records/",
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert_record(content[0], db)

def test_update_record(
    client: TestClient, db: Session
) -> None:
    record_db = create_record_in_db(db)

    data = {
        "title": "The Dark Side of the Moon",
        "img": "https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png",
    }
    response = client.put(
        f"/api/v1/records/{record_db.id}",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert_record(content, db)

def test_delete_record(
    client: TestClient, db: Session
) -> None:
    record_db = create_record_in_db(db)
    response = client.delete(
        f"/api/v1/records/{record_db.id}",
    )
    assert response.status_code == 200
    record = db.query(RecordDb).filter(RecordDb.id == record_db.id).first()
    assert record is None


def test_invalid_url(
    client: TestClient, db: Session
) -> None:
    data = {
        "title": "The Dark Side of the Moon",
        "img": "invalid_url",
    }
    response = client.post(
        "/api/v1/records/",
        json=data,
    )
    assert response.status_code == 422

def test_invalid_id(
    client: TestClient, db: Session
) -> None:
    response = client.get(
        f"/api/v1/records/invalid_id",
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["msg"] == "value is not a valid integer"

def test_invalid_id_update(
    client: TestClient, db: Session
) -> None:
    data = {
        "title": "The Dark Side of the Moon",
        "img": "https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png",
    }
    response = client.put(
        f"/api/v1/records/invalid_id",
        json=data,
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["msg"] == "value is not a valid integer"

def test_invalid_id_delete(
    client: TestClient, db: Session
) -> None:
    response = client.delete(
        f"/api/v1/records/invalid_id",
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["msg"] == "value is not a valid integer"


def test_invalid_title(
    client: TestClient, db: Session
) -> None:
    data = {
        "title": "",
        "img": "https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png",
    }
    response = client.post(
        "/api/v1/records/",
        json=data,
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["msg"] == "ensure this value has at least 1 characters"

def test_invalid_title_update(
    client: TestClient
) -> None:
    data = {
        "title": "",
        "img": "https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png",
    }
    response = client.put(
        f"/api/v1/records/1",
        json=data,
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["msg"] == "ensure this value has at least 1 characters"

def test_invalid_title_too_long(
    client: TestClient, db: Session
) -> None:
    data = {
        "title": "a" * 101,
        "img": "https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png",
    }
    response = client.post(
        "/api/v1/records/",
        json=data,
    )
    assert response.status_code == 422
    content = response.json()
    assert content["detail"][0]["msg"] == "ensure this value has at most 100 characters"
