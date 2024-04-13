from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class ExhibitSchema(BaseModel):
    name: Optional[str]
    exh_id : Optional[int]
    type_id: Optional[int]
    desc: Optional[str]
    url: Optional[str]
    timestamp: Optional[int]
    image_path: Optional[str]

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