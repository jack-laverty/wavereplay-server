from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import videos
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing wavepool videos and clips",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


@app.on_event("startup")
async def startup_event():
    from app.database import supabase
    try:
        # Simple query to test connection - just get one row
        response = supabase.table("clips").select("*").limit(1).execute()
        print(f"sent a query to test connection, received response: {response}")
        print(f"Successfully connected to Supabase in {settings.ENVIRONMENT} environment")
    except Exception as e:
        print(f"Failed to connect to Supabase: {e}")
        raise e


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    )
