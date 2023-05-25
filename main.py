import uvicorn
from fastapi import APIRouter, FastAPI

from api.handlers import quiz_router

app = FastAPI(title='Quiz')

main_api_router = APIRouter()
main_api_router.include_router(quiz_router)
app.include_router(main_api_router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
