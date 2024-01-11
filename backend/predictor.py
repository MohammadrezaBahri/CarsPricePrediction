import pandas as pd
import torch 


def predict(new_data_point: dict, pipeline) -> int:

    # Convert the new data point to a DataFrame
    new_data_point_df = pd.DataFrame(new_data_point, index=[0])
    
    # Make predictions on the new data point
    prediction = pipeline.predict(new_data_point_df)

    # Print or use the prediction as needed
    return int(prediction[0])

def dl_predict(new_data_point, preprocessor, model, device):
    new_data_point_df = pd.DataFrame(new_data_point, index=[0])
    new_data_point_processed = preprocessor.transform(new_data_point_df)
    new_data_point_tensor = torch.tensor(new_data_point_processed, dtype=torch.float32, device=device)

    with torch.no_grad():
        model.eval()
        return int(model(new_data_point_tensor).item())