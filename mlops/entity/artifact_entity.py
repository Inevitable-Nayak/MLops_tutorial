from dataclasses import dataclass
@dataclass
class dataingestionartifact:
    trained_file_path:str
    test_file_path:str
@dataclass    
class datavalidationartifact:
    validationstatus:bool
    valid_train_path:str
    invalid_train_path:str
    valid_test_path:str
    invalid_train_path:str
    drift_report_path:str
@dataclass    
class datatransformationartifact:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str
@dataclass      
class classificationmetricsartifact:
    f1_score:float
    recall_score:float
    precision_score:float
@dataclass
class modeltrainerartifact:
    trained_model_file_path:str
    train_metrics_artifact:classificationmetricsartifact
    test_metrics_artifact:classificationmetricsartifact
              
    