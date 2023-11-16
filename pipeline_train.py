import warnings

import hopsworks

import xgboost as xgb
from sklearn.metrics import f1_score

from utils import handler_features, handler_model

# Mute warnings
warnings.filterwarnings("ignore")

project = hopsworks.login()

fs = project.get_feature_store()

# get the feature view
feature_view = handler_features.get_view(fs)

# get the data splits
X_train, X_test, y_train, y_test = handler_features.get_splits(feature_view)

# define and train the model
model = xgb.XGBClassifier()
model.fit(X_train.values, y_train)

# test the model
y_pred_test = model.predict(X_test.values) # NOTE: test data are used

handler_model.test(y_test, y_pred_test)

# register the model
model_schema = handler_model.make_model_schema(X_train, y_train)
metrics = {
    "f1_score": f1_score(y_test, y_pred_test, average='macro')
}

handler_model.register(project, model, model_schema, metrics, input_example=X_train.sample())
