from sqlalchemy import Column, Integer, String
from db.config import Base


from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import mapped_column

EMBEDDING_SIZE = 640



class ExhibitModel(Base): 
    "Data model for exhibit"
    __tablename__ = "exhibit"

    id = Column(String, primary_key=True)
    exh_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)  
    type_id = Column(String, nullable=True) 
    description = Column(String, nullable=True)
    timestamp = Column(Integer, nullable=True) 
    embedding = mapped_column(Vector(EMBEDDING_SIZE))  


# СПЕЦИАЛЬНО НЕ СТАЛИ ДЕЛАТЬ РАЗВЕРНУТЮ СИСТЕМУ ХРАНЕНИЯ ДАННЫХ В БД.
# РЕШИЛИ СОСРЕДОТОЧИТЬСЯ НА МОДЕЛИ НЕЖЕЛИ НА БЭКЕНДЕ. А ТАК ВСЕ ЗНАЕМ, ВСЁ МОЖЕМ, ВСЕ УМЕЕМ :).

# class ExhibitTypeModel(Base): 
#     "Data model for exhibit type"
#     __tablename__ = "exhibit_type"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=True)  
#     desc = Column(String, nullable=True)  

#     exhibits = relationship("ExhibitModel", back_populates="exhibit_type", cascade="all,delete")

# class ImageModel(Base):
#     '''Data model for Image of exhibit'''
#     __tablename__ = "image"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=True)  
#     url = Column(String, nullable=True) 
#     timestamp = Column(Integer, nullable=True) 
#     path = Column(String, nullable=True)
#     embedding = mapped_column(Vector(EMBEDDING_SIZE))
      

#     exhibit_id = Column(Integer, ForeignKey('exhibit.id'))
#     exhibits = relationship("ExhibitModel", back_populates="images", cascade="all,delete")


