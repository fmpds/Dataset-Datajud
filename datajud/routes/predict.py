from fastapi import APIRouter
from datajud.controllers.predict import PredictController

router = APIRouter(prefix="/predict", tags=["predict"])

@router.get("/")
async def predict(data: dict):
    predict_controller = PredictController()
    return predict_controller.predict()
