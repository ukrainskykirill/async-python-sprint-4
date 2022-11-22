from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
import uvicorn
from src.api import base
from src.core.config import app_settings


app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(base.router, prefix='/api/v1')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    host = request.client.host
    if host in app_settings.blocked_host:
        return ORJSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                              content={"message": "Oops! Access forbidden! Your host in blocked list..."})
    response = await call_next(request)
    return response

if __name__ == '__main__':
    uvicorn.run(app, host=app_settings.host, port=app_settings.port)
