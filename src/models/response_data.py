
from pydantic import BaseModel
from datetime import datetime

class ResponseData(BaseModel):
    status: str
    message: str
    timestamp: datetime