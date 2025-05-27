# api/schemas/common.py
from typing import TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel
from pydantic import ConfigDict

DataT = TypeVar("DataT")

# 모든 API 가 사용하는 공통 응답 구조
class StandardResponse(GenericModel, Generic[DataT]):
    isSuccess: bool
    code: str
    message: str
    result: DataT

    model_config = ConfigDict(from_attributes=True)
