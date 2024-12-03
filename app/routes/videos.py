from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import logging
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)


class VideoCreate(BaseModel):
    title: str
    url: str
    recording_timestamp: datetime
    duration: float
    created_at: Optional[datetime] = None
    order_in_session: Optional[int] = None
    file_size: int
    file_format: str
    resolution: str
    session: int


class VideoResponse(BaseModel):
    id: int
    title: str
    url: str
    recording_timestamp: datetime
    duration: float
    created_at: datetime
    order_in_session: Optional[int]
    file_size: int
    file_format: str
    resolution: str
    session: int

    class Config:
        from_attributes = True


logger = logging.getLogger(__name__)

app = FastAPI()

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.post("/", response_model=VideoResponse)
async def create_video(video: VideoCreate):
    try:
        logger.debug(video)
        return video

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create video record: {str(e)}"
        )


@router.get("/{video_id}")
async def get_video(video_id: int):
    try:
        result = supabase.table('fastapi_test').select("*").eq('id', video_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Video not found")

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve video: {str(e)}"
        )


@router.get("/")
async def hellow():
    return {'message': [url, key]}
