from fastapi import APIRouter,Depends,status
from schema import Owner as SchemaOwner
from sqlalchemy.orm import Session
from schema import Audio as SchemaAudio
from queries.dialect_database_apis import DbApisQueries
from database.models import get_db
router = APIRouter()



@router.post("/add-owner/", status_code=status.HTTP_201_CREATED,response_model=SchemaOwner)
def add_owner(owner: SchemaOwner,db: Session = Depends(get_db)):
    return DbApisQueries.add_owner(owner,db)
@router.get("/owners/")
def get_all_owner(db: Session = Depends(get_db)):
    return DbApisQueries.get_all_owner(db)    