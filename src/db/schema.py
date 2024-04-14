from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class ExhibitSchema(BaseModel):
    name: Optional[str]
    exh_id : Optional[int]
    description: Optional[str]

    class Config:
        orm_mode = True

class TextSchema(BaseModel):
    text: Optional[str]
    
    class Config:
        orm_mode = True

class IdSchema(BaseModel):
    id: Optional[str]
    
    class Config:
        orm_mode = True

class PaginationSchema(BaseModel):
    limit: Optional[int] = 50
    offset: Optional[int] = 0
    class Config:
        orm_mode = True

# class GetPipesSchema(PipeSchema):
#     id: uuid4


# class Route(BaseModel):
#     robotId: str
#     name: Optional[str]
#     desc: Optional[str]
#     length: Optional[float]
#     timeDuration: Optional[str]

# class ChangeDefect(BaseModel):
#     id: Optional[str]
#     type: Optional[str]
    

#     class Config:
#         orm_mode = True