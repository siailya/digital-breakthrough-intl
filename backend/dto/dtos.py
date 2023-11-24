from typing import List

from pydantic import BaseModel


class SingleClassifyDto(BaseModel):
    text: str


class PackageClassifyDto(BaseModel):
    texts: List[str]
