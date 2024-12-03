import os
import sys
import logging
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)


class CommentCreate(BaseModel):
    timestamp: str
    author: str
    content: str
    video: int
    avatar_url: Optional[str] = None


class CommentResponse(BaseModel):
    id: int
    created_at: datetime
    timestamp: str
    author: str
    content: str
    video: int
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


# Configure logging to print to console
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to see all debug logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # This ensures logs print to console
    ]
)

logger = logging.getLogger(__name__)


app = FastAPI()

router = APIRouter(prefix="/api/comments", tags=["comments"])


@router.post("/", response_model=CommentResponse)
async def create_comment(comment: CommentCreate):
    try:

        result = supabase.table('comments').insert({
            'timestamp': comment.timestamp,
            'author': comment.author,
            'content': comment.content,
            'video': comment.video,
            'avatar_url': comment.avatar_url
        }).execute()

        logger.debug(f"Supabase insertion result: {result}")

        if result.data:
            # Return the first (and only) inserted record
            # This should now include the generated ID
            return result.data[0]
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to create comment"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create comment: {str(e)}"
        )


@router.get("/{video_id}")
async def get_comments(video_id: int):
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
async def helloworld():
    return {'message': [url, key]}
