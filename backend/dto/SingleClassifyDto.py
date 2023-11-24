from pydantic import BaseModel


class SingleClassifyDto(BaseModel):
    text: str