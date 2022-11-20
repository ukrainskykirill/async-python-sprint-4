from src.models.model import ShortUrl
from src.schemas.model import ShortUrlCreate
from .base import RepositoryDB


class RepositoryShortUrl(RepositoryDB[ShortUrl, ShortUrlCreate]):
    pass


url_crud = RepositoryShortUrl(ShortUrl)
