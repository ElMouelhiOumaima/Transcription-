from unittest.mock import Mock
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import get_db
from database.models import Base
from schema import Owner as SchemaOwner
from main import app
from configuration.config import DB_URL_test

SQLALCHEMY_DATABASE_URL = DB_URL_test
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_getowners ():
    res = client.get('/owners/')
    return res.json()

@pytest.mark.parametrize("name,id", [("asma", 1),("farah", 2),("tom", 3)])
def test_addowner(name, id):
        res = client.post("/add-owner/", json={"name" :name,"id":id})
        created_owner = SchemaOwner(**res.json())
        assert res.status_code == 201
        assert created_owner.name == name
        assert created_owner.id == id
        
