import uvicorn
from fastapi import FastAPI, APIRouter, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import os

from sqlalchemy import text


# from routers.video_router import VIDEO_PATH

app = FastAPI(version="0.3.0")

from db.config import engine, Base


app = FastAPI(
    docs_url=f"/docs",
    openapi_url="/api/openapi.json",
    # openapi_prefix='/api/'
)


from routers import file_router, exhibit_router


routers = [file_router, exhibit_router]

for router in routers:
    app.include_router(router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/api/images/', StaticFiles(directory=os.path.join('/',*os.getcwd().split('/')[:-2],'data','images')))


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.execute(text('DROP SCHEMA public CASCADE;'))
        # await conn.execute(text('CREATE SCHEMA public;'))
        # await conn.execute(text('GRANT ALL ON SCHEMA public TO postgres;'))
        # await conn.execute(text('GRANT ALL ON SCHEMA public TO public;'))

        # await conn.execute(text('CREATE EXTENSION IF NOT EXISTS pg_trgm;'))
        # await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector;'))

        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        
        
        pass


if __name__ == "__main__":
    uvicorn.run("app:app", host="109.248.175.95")