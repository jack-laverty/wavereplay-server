from fastapi import FastAPI
from app.routes import videos
from app.routes import comments
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing database and file storage access for wave replay",
    version="1.0.0"
)

app.include_router(videos.router)
app.include_router(comments.router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    )
