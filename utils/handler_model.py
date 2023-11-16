import os
import joblib

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix

from hsml.schema import Schema
from hsml.model_schema import ModelSchema

model_dir="model"

def make_model_schema(X_train, y_train):

    input_schema = Schema(X_train.values)
    output_schema = Schema(y_train)
    model_schema = ModelSchema(input_schema=input_schema, output_schema=output_schema)

    model_schema.to_dict()

    return model_schema


def register(project, model, model_schema, metrics, input_example):

    if os.path.isdir(model_dir) == False:
        os.mkdir(model_dir)

    joblib.dump(model, model_dir + '/xgboost_fraud_batch_model.pkl')
    
    mr = project.get_model_registry()

    fraud_model = mr.python.create_model(
        name="xgboost_fraud_batch_model", 
        metrics=metrics,
        model_schema=model_schema,
        input_example=input_example, 
        description="Fraud Batch Predictor",
    )

    fraud_model.save(model_dir)

    pass

def test(y_test, y_pred_test):

    results = confusion_matrix(y_test, y_pred_test)
    print(results)

    df_cm = pd.DataFrame(
        results, 
        ['True Normal', 'True Fraud'],
        ['Pred Normal', 'Pred Fraud'],
    )

    cm = sns.heatmap(df_cm, annot=True)
    cm.get_figure()

    plt.show()