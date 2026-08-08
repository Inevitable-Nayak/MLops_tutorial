from mlops.entity.artifact_entity import classificationmetricsartifact
from mlops.exception.exception import customexception
import sys,os
from sklearn.metrics import f1_score,precision_score,recall_score
def get_classification_score(y_true,y_pred)->classificationmetricsartifact:
    try:
        model_f1_score=f1_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)
        mode_precision_score=precision_score(y_true,y_pred)
        classification_metrics=classificationmetricsartifact(
            f1_score=model_f1_score,
            recall_score=model_recall_score,
            precision_score=mode_precision_score
        )
        return classification_metrics
    except Exception as e:
        raise customexception(e,sys)