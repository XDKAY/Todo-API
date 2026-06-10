from typing import Annotated

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: Annotated[int, Field(default=9, ge=0, le=100)]
    offset: Annotated[int, Field(default=0, ge=0)]
