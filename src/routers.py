from typing import List, Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy import select, delete, update, text, func
from sqlalchemy.orm import selectinload, joinedload, subqueryload, contains_eager, defer

from dependencies import get_session
from db.config import async_session

from db.model import ExhibitModel
from db.schema import *

import aiofiles
from random import randint
import time
import uuid
import requests
import os
import numpy as np
import json
import base64

ML_SEARCH_API_URL = 'http://194.87.158.79:51009/post'


exhibit_router = APIRouter(
    prefix="/api/exhibits",
    tags=["Exhibits"],
)

file_router = APIRouter(
    prefix="/api/files",
    tags=["Files"],
)

@exhibit_router.get("/find_by_id", status_code=200)
async def find_images_by_id(data: IdSchema = Depends(), session: async_session = Depends(get_session)):
        image_path = os.path.join('/',*os.getcwd().split('/')[:-2],'data','images',f'{data.id}.jpg')
        async with aiofiles.open(image_path, 'rb') as out_file:
            image_data = await out_file.read()
            blob_image = base64.b64encode(image_data)

        emb_json = json.dumps({"data": [
                        {
                        "blob": blob_image.decode('utf-8')
                        }
                    ],
                    "targetExecutor":"clip_t",
                    "parameters": {}
                    })
        r = requests.post(ML_SEARCH_API_URL, data=emb_json, headers={'Content-Type': 'application/json'})
        emb = json.loads(r.content)
        q = text(f"SELECT id, name, type_id, description, 1-('{emb['data'][0]['embedding']}'<=> embedding) AS cosine_similarity FROM exhibit ORDER BY cosine_similarity DESC LIMIT 10")
        result = await session.execute(q)
        result = result.mappings().all()

        return { 'id':data.id,
                'type_id':'Не определен',
                'similar': result}




@exhibit_router.post("/find_by_image", status_code=200)
async def find_images_by_image(files: List[UploadFile] = File(...), session: async_session = Depends(get_session)):
    for i,f in enumerate(files):
        image_uuid = str(uuid.uuid4())
        image_path = os.path.join('/',*os.getcwd().split('/')[:-2],'data','images',f'{image_uuid}.jpg')
        async with aiofiles.open(image_path, 'wb') as out_file:
            content = await f.read()  # async read
            blob_image = base64.b64encode(content)
            await out_file.write(content) 

        emb_json = json.dumps({"data": [
                        {
                        "blob": blob_image.decode('utf-8')
                        }
                    ],
                    "targetExecutor":"clip_t",
                    "parameters": {}
                    })
        r = requests.post(ML_SEARCH_API_URL, data=emb_json, headers={'Content-Type': 'application/json'})
        emb = json.loads(r.content)
        q = text(f"SELECT id, name, type_id, description, 1-('{emb['data'][0]['embedding']}'<=> embedding) AS cosine_similarity FROM exhibit ORDER BY cosine_similarity DESC LIMIT 10")
        result = await session.execute(q)
        data = result.mappings().all()

        return { 'id':image_uuid,
                'type_id':'Не определен',
                'similar': data}
    
@exhibit_router.post("/find_by_text", status_code=200)
async def find_images_by_text(data: TextSchema, session: async_session = Depends(get_session)):
        emb_json = json.dumps({"data": [
                        {
                        "text": data.text
                        }
                    ],
                    "targetExecutor":"clip_t",
                    "parameters": {}
                    })
        r = requests.post(ML_SEARCH_API_URL, data=emb_json, headers={'Content-Type': 'application/json'})
        emb = json.loads(r.content)
        q = text(f"SELECT id, name, type_id, description, 1-('{emb['data'][0]['embedding']}'<=> embedding) AS cosine_similarity FROM exhibit ORDER BY cosine_similarity DESC LIMIT 10")
        result = await session.execute(q)
        result = result.mappings().all()

        return { 'text':data.text,
                'type_id':'Не определен',
                'similar': result}
                
@exhibit_router.post("/test_text", status_code=200)
async def test_text(data: TextSchema = Depends(), session: async_session = Depends(get_session)):
        columns = func.coalesce(ExhibitModel.description, '').concat(func.coalesce(ExhibitModel.name, ''))
        columns = columns.self_group()

        term = data.text
        # q = select(ExhibitModel.description,ExhibitModel.name,func.similarity(columns, term)).where(columns.bool_op('%')(term),).order_by(func.similarity(columns, term).desc(),)
        
        term = 'search string'
        q = select(ExhibitModel.name,func.similarity(ExhibitModel.name, term), ).where(ExhibitModel.name.bool_op('%')(term),).order_by(func.similarity(ExhibitModel.name, term).desc(), )
        result = await session.execute(q)

        result = result.mappings().all()
        print(result)


@exhibit_router.post("/add")
async def add_image_in_database(exhibit: ExhibitSchema = Depends(), files: List[UploadFile] = File(...), session: async_session = Depends(get_session), ):
    for i,f in enumerate(files):
        image_uuid = str(uuid.uuid4())
        image_path = os.path.join('/',*os.getcwd().split('/')[:-2],'data','images',f'{image_uuid}.jpg')
        async with aiofiles.open(image_path, 'wb') as out_file:
            content = await f.read()  # async read
            blob_image = base64.b64encode(content)
            await out_file.write(content)

        new_exhibit = ExhibitModel(**exhibit.dict())
        new_exhibit.id = image_uuid
        new_exhibit.type_id = 'Тип не указан'
        new_exhibit.timestamp = int(time.time())
        emb_json = json.dumps({"data": [
                        {
                        "blob": blob_image.decode('utf-8')
                        }
                    ],
                    "targetExecutor":"clip_t",
                    "parameters": {}
                    })
        r = requests.post(ML_SEARCH_API_URL, data=emb_json, headers={'Content-Type': 'application/json'})
        emb = json.loads(r.content)

        new_exhibit.embedding = emb['data'][0]['embedding']

        session.add(new_exhibit)
        await session.commit()
    return {"status": "200"}



@exhibit_router.get("", status_code=200)
async def get_all_images(pagination: PaginationSchema = Depends(), session: async_session = Depends(get_session)):
    q = select(ExhibitModel).options(defer(ExhibitModel.embedding)).offset(pagination.offset).limit(pagination.limit)
    result = await session.execute(q)
    data = result.scalars().all()
    return data

@exhibit_router.get("/image_counts", status_code=200)
async def get_image_counts(session: async_session = Depends(get_session)):
    q = select(func.count()).select_from(ExhibitModel)
    result = await session.execute(q)
    print(result)
    data = result.scalars().first()
    return data

@exhibit_router.get("/{id}", status_code=200)
async def get_imag_info_by_id(id, session: async_session = Depends(get_session)):
    q = select(ExhibitModel).where(ExhibitModel.id==id).options(defer(ExhibitModel.embedding))
    result = await session.execute(q)
    data = result.scalars().first()
    return data

