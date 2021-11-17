import pandas as pd
import numpy as np
import re
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

SEVERITY_MAPPING = joblib.load("models/severity_category_mapping.pkl")
COMPONENT_MAPPING =  joblib.load("models/component_name_mapping.pkl")


class Product_classifier():

    def __init__(self, model:TfidfVectorizer, vectorizer:RandomForestClassifier):

        
        self.model = model
        self.vectorizer = vectorizer

    def _custom_tokenizer(self,text:str): 
        tokens=[]
        for token in text.split(" "):
            tmp=[ (sub_word) for _token in token.split(".") for sub_word in _token.split("_")]
            tokens.extend(tmp)                    
        return " ".join(tokens)


    def _preprocess_data(
        self,
        short_description:str,
        long_description:str,
        severity_category:str,
        component_name:str,
    ):
        test_df =  pd.DataFrame(
            [{"short_description":short_description,
            "long_description" :long_description,
            "severity_category":severity_category,
            "component_name":component_name
            }]
         )

        test_df["severity_category"] = test_df.severity_category.apply(lambda x: SEVERITY_MAPPING.get(x.lower(),1))

        test_df["component_name"] = test_df.component_name.map(lambda x: COMPONENT_MAPPING.get(x.lower(),1))

        test_df["short_description"] = test_df.short_description.apply(lambda x : re.sub(r'[\[\]]',"" ,x))

        test_df["short_description"] = test_df.short_description.apply(self._custom_tokenizer)

        test_df.long_description = test_df.long_description.apply(lambda x : re.sub(r'[\[\]]',"" ,x))

        test_df.long_description = test_df.long_description.apply(self._custom_tokenizer)

        test_df["text"]=test_df.apply(lambda x: "SHORT DESCRIPTION " + x["short_description"]+\
                        ". LONG DESCRIPTION "  + x["long_description"] , axis=1)

        return test_df

    def _create_features(self,test_df:pd.DataFrame):
        test_tf_vec = self.vectorizer.transform(test_df.text)
        tab_feature = ['component_name',  'severity_category']
        test_feat=np.hstack(( test_df[tab_feature].values ,\
         test_tf_vec.toarray()
        ))

        return test_feat


    def get_predictions(
        self, 
        short_description:str,
        long_description:str,
        severity_category:str,
        component_name:str,
        ):
    
        test_df = self._preprocess_data(short_description,long_description,severity_category,component_name )
        test_features = self._create_features(test_df)
        prediction = self.model.predict(test_features)[0]

        return prediction