from fastapi import APIRouter
from datajud.controllers.predict import PredictController

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("/")
async def predict(data: dict):
    # the data will be the process table in the processo table    
    predict_controller = PredictController()
    return predict_controller.predict(data)
