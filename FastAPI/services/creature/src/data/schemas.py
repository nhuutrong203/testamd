from pydantic import BaseModel

class CreatureBase(BaseModel):
    name: str
    country: str
    area:str
    description: str
    aka:str
    explorer_id:int

class CreatureCreate(CreatureBase):
    pass

class Creature(CreatureBase):
    id: int

    class Config:
        from_attributes = True

class UserInput(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    hash: str

class UserOutput(BaseModel):
    username: str

class User(UserOutput):
    id: int

    class Config:
        from_attributes = True
