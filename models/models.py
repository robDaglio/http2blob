from pydantic import BaseModel
from typing import Union

class Event(BaseModel):
    EventID: int
    DateTime: Union[str, None] = None
    Location: Union[str, None] = None
    Stage: str
    Product: str
