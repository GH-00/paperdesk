from fastapi import FastAPI

from app.api.dashboard import router as dashboard_router


app = FastAPI(
    title="Paperdesk API",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(
    dashboard_router,
    prefix="/api/v1",
)
