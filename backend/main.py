from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pandasai import SmartDataframe
import pandas as pd
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from src.services.gemini_service import gemini_service

# Load environment variables
load_dotenv()

app = FastAPI(title="Sales Data API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the data for PandasAI
df = pd.read_csv("src/datasets/sales_data_sample_cleaned.csv")
df = SmartDataframe(df)

class Query(BaseModel):
    question: str

@app.post("/query/pandasai")
async def query_data_pandasai(query: Query):
    try:
        response = df.chat(query.question)
        return {"result": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/query/ownmodel")
async def query_data_custom(query: Query):
    try:
        response = await gemini_service.query(query.question)
        return {"result": response}
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing query: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    