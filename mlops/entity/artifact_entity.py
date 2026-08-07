from dataclasses import dataclass
class dataingestionartifact:
    trained_file_path:str
    test_file_path:str
class datavalidationartifact:
    validationstatus:bool
    valid_train_path:str
    invalid_train_path:str
    valid_test_path:str
    invalid_train_path:str
    drift_report_path:str
class datatransformationartifact:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str    
    