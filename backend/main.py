from fastapi import FastAPI
import joblib
import torch
from .predictor import predict, dl_predict
from .schemas import Post, Prediction
from .model import CarPricePredictionModel

# Load the previously saved Transformer and XGBoost model
pipeline = joblib.load('backend/src/car_price_prediction_pipeline.joblib')

# Load the Deep Learning Model and Preprocessor
preprocessor = joblib.load('backend/src/preprocessor.joblib')
num_features = len(preprocessor.get_feature_names_out())
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = CarPricePredictionModel(num_features).to(device)
model.load_state_dict(torch.load('backend/src/model.pth'))

app = FastAPI()

@app.get("/predict/", response_model=Prediction)
def single_prediction(new_data_point: Post):
    return {
        "predicted_price": predict(new_data_point.model_dump(), pipeline),
        "dl_predicted_price": dl_predict(new_data_point.model_dump(), preprocessor, model, device)
        }

