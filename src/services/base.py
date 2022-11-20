import secrets
import string
from fastapi.encoders import jsonable_encoder
from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import select, update
from src.db.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def update_clicks(self, db: AsyncSession, short_url: str, clicks: int) -> None:
        statement = update(self._model).filter_by(short_url=short_url).values(clicks=clicks+1)
        await db.execute(statement=statement)
        await db.commit()

    async def get_clicks(self, db: AsyncSession, short_url) -> int:
        statement = select(self._model).where(self._model.short_url == short_url)
        obj = await db.scalar(statement=statement)
        clicks = obj.clicks
        return clicks

    async def get(self, db: AsyncSession, short_url: str) -> ModelType:
        statement = select(self._model.url).where(self._model.short_url == short_url)
        clicks = await self.get_clicks(db, short_url)
        await self.update_clicks(db=db, short_url=short_url, clicks=clicks)
        result = await db.scalar(statement=statement)
        return result

    async def get_status(self, db: AsyncSession, short_url: str) -> ModelType:
        statement = select(self._model).where(self._model.short_url == short_url)
        result = await db.execute(statement=statement)
        return result.scalar()

    async def get_user_status(self, db: AsyncSession, nickname: str) -> ModelType:
        statement = select(self._model).where(self._model.user.nikname == nickname)
        result = await db.scalars(statement)
        return result

    @staticmethod
    def short_url(length: int = 5) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(chars) for _ in range(length))

    async def post(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db_obj.short_url = self.short_url()
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def batch_upload(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        all_obj = []
        for obj in obj_in_data:
            db_obj = self._model(**obj)
            db_obj.short_url = self.short_url()
            all_obj.append(db_obj)
        db.add_all(all_obj)
        await db.commit()
        for obj in all_obj:
            await db.refresh(obj)
        return all_obj
