from typing import Annotated
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import yaml
router = APIRouter(prefix="/keyfa", tags=["KEY FastAPI Default"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/health")
async def get_health(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return "ok"

@router.get("/openapi.yaml", response_class=PlainTextResponse)
async def get_opnapi_yaml(request: Request):
    openapi_json = request.app.openapi()
    openapi_yaml = yaml.dump(openapi_json)
    return openapi_yaml