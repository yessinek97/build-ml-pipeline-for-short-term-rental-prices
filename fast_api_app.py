from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Value(BaseModel):
  value: int

class Data(BaseModel):
  feature_1: float
  feature_2: str

@app.post('/{path}')
async def exercise_function(path: int, query: int, body: Value):
  return {
    "path": path, 
    "query": query, 
    "body": body
}

@app.post("/data/")
async def ingest_data(data: Data):
    if data.feature_1 < 0:
        raise HTTPException(status_code=400, detail="feature_1 needs to be above 0.")
    if len(data.feature_2) > 280:
        raise HTTPException(
            status_code=400,
            detail=f"feature_2 needs to be less than 281 characters. It has {len(data.feature_2)}.",
        )
    return data
