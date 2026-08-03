import sys 
import os 
from mlops.logging.logger import logging
class customexception(Exception):
    def __init__(self,error_message,error_detail:sys):
        self.error_message=error_message
        _,_,exc_tb=error_detail.exc_info()
        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename
    def __str__(self):
        return f"Error occured in script: [{self.filename}] at line number: [{self.lineno}] error message: [{self.error_message}]"
if __name__=="__main__":
    try:
        a=1/0
        logging.info("not printing this line")
    except Exception as e:
        raise customexception(e,sys)        