from pydantic import BaseModel
class Audio(BaseModel):
    name: str
    duration: int
    owner_id: int

    class Config:
        orm_mode = True

class Audio_Update(Audio):
    pass


class Owner(BaseModel):
    name: str
    id:int
    class Config:
        orm_mode = True
