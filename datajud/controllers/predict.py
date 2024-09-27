import joblib
from pathlib import Path
import pandas as pd

class PredictController:
    def __init__(self):
        model_path = Path(__file__).parent.parent.joinpath('models').joinpath('ml_datajud.pkl')
        print(model_path)
        self.model = joblib.load(model_path)

    def predict(self, process_params):
        try:
            predict_df = pd.DataFrame([process_params])
            prediction = self.model.predict(predict_df)
        except Exception as error:
            print(f"An error occurred during prediction: {error}")
            raise error
        
        return prediction[0]
