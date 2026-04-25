"""intimoi backend application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="intimoi API",
        version="0.1.0",
        description="intimoi 小程序后端服务",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    from app.api.v1 import router as v1_router
    app.include_router(v1_router, prefix="/api/v1")

    return app
