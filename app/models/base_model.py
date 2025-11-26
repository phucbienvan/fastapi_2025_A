import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import as_declarative

@as_declarative()
class Base:
    __abstract__ = True
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class BaseModel(Base):
    __abstract__ = True
    id: int = Column(Integer, primary_key=True, index=True)
