from fastapi import FastAPI
from data_tools.endpoints import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(title="Video Processing API")
    app.include_router(api_router)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
