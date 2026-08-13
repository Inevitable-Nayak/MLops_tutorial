import sys
import os
import  certifi
ca= certifi.where()
from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_db_url")
print(mongo_db_url)
import pymongo
from mlops.logging.logger import logging
from mlops.exception.exception import customexception
from mlops.pipeline.training_pipeline import trainingpipeline
import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app.add_middleware(
    CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"]
)
from fastapi import File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from mlops.constants.training_pipeline import data_ingestion_database_name
from mlops.constants.training_pipeline import data_ingestion_collection_name
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database=client[data_ingestion_database_name]
collection=client[data_ingestion_collection_name]
@app.get("/",tags=["authetication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get("/train")
async def train_route():
    try:
        train_pipeline=trainingpipeline()
        train_pipeline.run_pipeline()
        return Response("training is succesfull")
    except Exception as e:
        raise customexception(e,sys)


