from datetime import datetime
from pydantic import BaseModel


class ShortUrlBase(BaseModel):
    url: str


class ShortUrlCreate(ShortUrlBase):
    pass


class ShortUrlCreateBatchUpload(BaseModel):
    __root__: list[ShortUrlBase]


class ShortUrlInDBBase(ShortUrlBase):
    id: int
    url: str
    short_url: str
    clicks: int
    created_at: datetime

    class Config:
        orm_mode = True


class ShortUrl(ShortUrlInDBBase):
    pass


class ShortUrlInDB(ShortUrlInDBBase):
    pass


class ShortUrlBatchUploadResponse(BaseModel):
    __root__: list[ShortUrlInDBBase]
