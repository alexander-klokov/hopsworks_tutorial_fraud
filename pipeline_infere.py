import joblib
import hopsworks

version_model=2
version_feature_view=1

num_to_display=11

# login to hopsworks and get access to the feature store
project = hopsworks.login()
fs = project.get_feature_store()

# retrieve the model
mr = project.get_model_registry()

retrieved_model = mr.get_model(name="xgboost_fraud_batch_model", version=version_model)

saved_model_dir = retrieved_model.download()
retrieved_xgboost_model = joblib.load(saved_model_dir + "/xgboost_fraud_batch_model.pkl")

# get data
feature_view = fs.get_feature_view(name='transactions_view_fraud_batch_fv', version=version_feature_view)
feature_view.init_batch_scoring(1)

batch_data = feature_view.get_batch_data()
batch_data.drop(["datetime"], axis=1, inplace=True)
print(batch_data.head(num_to_display))

# make predictions
predictions = retrieved_xgboost_model.predict(batch_data)

print("Predicted: ", predictions[:num_to_display])