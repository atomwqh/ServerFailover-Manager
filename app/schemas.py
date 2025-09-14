from pydantic import BaseModel

class GroupBase(BaseModel):
    name: str
    script: str

class GroupCreate(GroupBase):
    pass

class GroupRead(GroupBase):
    id: int
    class Config:
        orm_mode = True

class ServerBase(BaseModel):
    ip: str
    group_id: int

class ServerCreate(ServerBase):
    pass

class ServerRead(ServerBase):
    id: int
    class Config:
        orm_mode = True
