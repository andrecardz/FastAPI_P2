from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.base import Base
from app.database.session import engine
from app.routes.produtos import router as produtos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API de Produtos", lifespan=lifespan)
app.include_router(produtos_router)
