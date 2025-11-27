from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from story_generator import StoryGenerator

app = FastAPI(title="AI Story Game API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize story generator
story_gen = StoryGenerator()


class StartGameRequest(BaseModel):
    theme: Optional[str] = "adventure"


class ActionRequest(BaseModel):
    story_id: str
    action: str  # การกระทำของผู้เล่น เช่น "เดินไปทางซ้าย", "สำรวจหีบสมบัติ"


class StoryResponse(BaseModel):
    story_id: str
    narrative: str
    directions: List[str] = []  # ทิศทางที่ไปได้
    objects: List[str] = []     # สิ่งของที่สำรวจได้
    hint: str = ""              # คำแนะนำ
    inventory: List[str] = []   # สิ่งของในกระเป๋า
    is_ending: bool


@app.get("/")
async def root():
    return {"message": "AI Story Game API", "status": "running"}


@app.post("/api/game/start", response_model=StoryResponse)
async def start_game(request: StartGameRequest):
    try:
        result = await story_gen.start_story(request.theme)
        return result
    except Exception as e:
        import traceback
        print(f"Error in start_game: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/game/action", response_model=StoryResponse)
async def make_action(request: ActionRequest):
    try:
        result = await story_gen.continue_story(
            request.story_id,
            request.action
        )
        return result
    except Exception as e:
        import traceback
        print(f"Error in make_action: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/game/themes")
async def get_themes():
    return {
        "themes": [
            {"id": "adventure", "name": "ผจญภัย", "description": "การผจญภัยในโลกแฟนตาซี"},
            {"id": "mystery", "name": "ลึกลับ", "description": "ไขปริศนาสุดระทึก"},
            {"id": "scifi", "name": "ไซไฟ", "description": "อนาคตและเทคโนโลยี"},
            {"id": "horror", "name": "สยองขวัญ", "description": "เรื่องราวสุดหลอน"},
            {"id": "romance", "name": "โรแมนติก", "description": "เรื่องราวความรัก"},
            {"id": "fantasy", "name": "แฟนตาซี", "description": "โลกแห่งเวทมนตร์และสิ่งมหัศจรรย์"},
            {"id": "drama", "name": "ดราม่า", "description": "เรื่องราวเข้มข้นสะเทือนอารมณ์"},
        ]
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
