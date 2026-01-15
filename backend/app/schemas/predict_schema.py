from pydantic import BaseModel

class TrafficInput(BaseModel):
    data: dict