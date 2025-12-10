from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Optional


T = TypeVar("T")

class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''

    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        return self
    
class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def custom_response(cls, code: str, message: str, data: T):
        return cls(code=code, message=message, data=data)
    
    @classmethod
    def success_response(cls, data: T):
        return cls(code='000', message='success', data=data)
