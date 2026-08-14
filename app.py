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
from mlops.utils.main_utils.utils import load_object
from mlops.utils.ml_utils.model.estimator import networkmodel
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
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database=client[data_ingestion_database_name]
collection=client[data_ingestion_collection_name]
@app.get("/",tags=["authetication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get("/train")
async def train_route():

    try:

        train_pipeline = trainingpipeline()

        model_trainer_artifact = (
            train_pipeline.run_pipeline()
        )

        return {
            "message": "Training successful",
            "model": str(
                model_trainer_artifact.trained_model_file_path
            )
        }

    except Exception as e:

        raise customexception(e, sys)
@app.post("/predict")
async def predict(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model= networkmodel(preprocessor=preprocessor,model=final_model)
        y_pred=network_model.predict(df)
        df['predicted_coloumn']=y_pred
        df.to_csv('predicted_output/output.csv')
        table_html=df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html",{"request":Request,"table":table_html})
    except Exception as e:
        raise customexception(e,sys)
    



