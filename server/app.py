from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager

from keyfa.config import Config
from keyfa.util.importutil import import_keyfa

from keyfa.logmodule.logfactory import get_logger



@asynccontextmanager
async def lifespan(application: FastAPI):
    # on startup
    get_logger("uvicorn.access")
    yield

    # on shutdown
    

app = FastAPI(title="keyfa", lifespan=lifespan)
import_keyfa(app)

if __name__ == "__main__":
    uvicorn.run(
        app="__main__:app",
        host = Config.server.host,
        port = Config.server.port,
        reload=Config.server.reload
    )
