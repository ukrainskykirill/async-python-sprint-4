import logging.config
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.db import get_session
from src.schemas import model as schema
from src.services.short_url import url_crud
from src.core.logging import LOGGING

router = APIRouter()

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('api_logger')


@router.get('/ping')
async def get_db_status(
    *,
    db: AsyncSession = Depends(get_session)
) -> any:
    try:
        conn = await db.connection()
        if conn:
            logger.info('DB connection access established')
            return {'DB connection': 'Access established'}
    except Exception:
        logger.warning('DB coonection has no access')
        return {'DB connection': 'No access'}


@router.get('/{short_url}', response_model=list[schema.ShortUrl])
async def get_url(
        *,
        db: AsyncSession = Depends(get_session),
        short_url: str
) -> any:
    target = await url_crud.get(db=db, short_url=short_url)
    if not target:
        logger.info('URL not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='URL not found')
    return RedirectResponse(target)


@router.get('/{short_url}/status', response_model=schema.ShortUrl)
async def get_status_url(
        *,
        db: AsyncSession = Depends(get_session),
        short_url: str
) -> any:
    status = await url_crud.get_status(db=db, short_url=short_url)
    if not status:
        logger.warning('Item not found')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return status


@router.post("/url", response_model=schema.ShortUrl, status_code=status.HTTP_201_CREATED)
async def shor_url(
        *,
        db: AsyncSession = Depends(get_session),
        schema_in: schema.ShortUrlCreate
) -> any:
    short_url = await url_crud.create(db=db, obj_in=schema_in)
    logger.info('short URL created')
    return short_url


@router.post('/shorten', response_model=schema.ShortUrlBatchUploadResponse, status_code=status.HTTP_201_CREATED)
async def batch_upload(
        *,
        db: AsyncSession = Depends(get_session),
        schema_in: schema.ShortUrlCreateBatchUpload
) -> any:
    short_url = await url_crud.create_multi(db=db, obj_in=schema_in)
    logger.info('batch upload success')
    return short_url
