from fastapi import Depends, FastAPI,APIRouter, Request

from src.models.request_data import RequestData
from src.utils import Anazlyze_stock
from src.models.response_data import ResponseData
from datetime import datetime
chat = APIRouter()

def get_llm_client(request: Request):
    return {"llm": request.app.state.llm, "client": request.app.state.client}


@chat.post("/generate-text")
async def generate_text(data: RequestData,llm_dependency: dict = Depends(get_llm_client)):
    prompt = data.prompt
    response = Anazlyze_stock(prompt,llm_dependency)
    return ResponseData(status="success",message=response,timestamp=datetime.now())
