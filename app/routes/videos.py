from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.database import supabase

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("/")
async def list_videos() -> List[Dict]:
    try:
        response = supabase.table('videos').select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{video_id}")
async def get_video(video_id: int) -> Dict:
    try:
        response = supabase.table('videos').select("*").eq('id', video_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Video not found")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_video(video: Dict) -> Dict:
    try:
        response = supabase.table('videos').insert(video).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{video_id}")
async def delete_video(video_id: int) -> Dict:
    try:
        response = supabase.table('videos').delete().eq('id', video_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Video not found")
        return {"message": "Video deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
