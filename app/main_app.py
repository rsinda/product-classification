from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import wrapper

api_router = APIRouter()
api_router.include_router(
    wrapper.router, prefix="/predict", tags=["predict"])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="")

if __name__ == "__main__":
    uvicorn.run('main_app:app', host='0.0.0.0', port=8000, reload=False)



