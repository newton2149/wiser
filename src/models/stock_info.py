from pydantic import BaseModel, Field

class StockInfo(BaseModel):
    company: str = Field(..., description="Name of the company")
    ticker: str = Field(..., description="Ticker symbol of the company")