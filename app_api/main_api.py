from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from log.logger_config import logger
from routes.tree import router as tree_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🌱 API iniciada y lista para recibir solicitudes.")
    yield
    logger.info("🛑 API cerrándose.")


app = FastAPI(title="--", description="--", version="1.0.0", lifespan=lifespan)


app.include_router(tree_router, prefix="/v1.0.0", tags=["Agent Execution"])
