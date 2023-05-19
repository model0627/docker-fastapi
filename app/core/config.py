from pathlib import Path

#from aiocronjob.job import JobInfo
from fastapi import FastAPI, HTTPException, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware

## 커스텀
from core.scheduler import cronjob_schedulers_running

#from event.router import router as EventRouter 


tags_metadata = [
    {
        "name": "FastAPI",
        "description": "",
        "externalDocs": {
            "description": "👉 운영 명세서에요.",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(title="REPORT REST API", 
              description="""
                Fast API 🚀 

                ## 작성자 : 
                """,
              version="0.0.1",
              openapi_tags=tags_metadata)

api_router = APIRouter()

origins = [
    "http://localhost",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 신규 URI
#app.include_router(EventRouter, tags=["EVENT"], prefix="/analyze")

# 배치 스케줄, 크론 작업 실행, 기동 시 수행
cronjob_schedulers_running()

static_dir = Path(__file__).parent.joinpath("build").absolute()

