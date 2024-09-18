from fastapi import FastAPI
import uvicorn

from datajud.routes.predict import router as predict_router
from datajud.routes.import_process import router as import_router

app = FastAPI()

app.include_router(predict_router)
app.include_router(import_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)