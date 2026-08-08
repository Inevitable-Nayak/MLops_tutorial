import yaml
from mlops.exception.exception import customexception
from mlops.logging.logger import logging
import os, sys
import numpy as np
#import dill
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
def read_yaml_file(file_path: str) -> dict:

    try:
       with open(file_path, "rb") as yaml_file:
           return yaml.safe_load(yaml_file)
    except Exception as e:
       raise customexception(e, sys) 
def write_ymal_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w')as file:
            yaml.dump(content,file)
    except Exception as e:
        raise customexception(e,sys)
def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise customexception(e,sys) 
def save_object(file_path:str,obj:object):
    try:
        logging.info("save the object")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("exited the save object ")    
    except Exception as e:
        raise customexception(e,sys)
def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception("the file is missing ")
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)    
    except Exception as e:
        raise customexception(e,sys)
def load_numpy_array(file_path:str)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise customexception(e,sys)
def evaluate_models(x_train,y_train,x_test,y_test,models,param):
    try:
        report={}
        for i in range(len(list(models))):              
            para=param[list(models.keys())[i]]
            gs=GridSearchCV(models,para,cv=3)
            gs.fit(x_train,y_train)
            models.set_params(**gs.best_params_)
            models.fit(x_train,y_train)
            y_train_pred=models.predict(x_train)
            y_test_pred=models.predict(y_test)
            train_model_score=r2_score(y_train_pred,y_test_pred)
            test_model_score=r2_score(y_train_pred,y_test_pred)
            report[list(models.keys())[i]]=test_model_score
        return report
    except Exception as e:
        raise customexception(e,sys)
    