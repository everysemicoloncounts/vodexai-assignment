import uvicorn
from fastapi import FastAPI
from app.api.Items.endpoints import router as items_router

app = FastAPI()

app.include_router(items_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")