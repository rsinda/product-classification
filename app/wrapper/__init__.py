from typing import Any
from fastapi import APIRouter,Query
from pydantic import BaseModel
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from wrapper.core import Product_classifier 

TFIDF_vectorizer = joblib.load("models/tf_vectorizer.pkl")
RF_MODEL = joblib.load("models/model.pkl")

classifier = Product_classifier(model=RF_MODEL,vectorizer=TFIDF_vectorizer)
router = APIRouter()

class ResponseModel(BaseModel):
    product_name: Any

class RequestModel(BaseModel):
    short_description: str = "Regression There are two extra lines when preview the sample report in PDF 0301 1200"
    long_description: str="""Created attachment 103916
report design

Description:
There are two extra lines when preview the sample report in PDF 

Build number:
2 3 0 v20080606-1648

Steps to reproduce:
1  Preview the attached report design as PDF 

Expected result:
The report works correctly in PDF 

Actual result:
See the screenshot 

Error log:
N/A"""
    component_name:str="Report Engine"

@router.post("/", response_model=ResponseModel)
def predict(query: RequestModel,severity_category:str= Query('normal', enum=['normal', 'blocker', 'trivial', 'minor', 'major', 'critical'])) -> Any:
    results = classifier.get_predictions(
        short_description=query.short_description, long_description=query.long_description,
        severity_category=severity_category, component_name=query.component_name
        )

    return  {"product_name":results}
