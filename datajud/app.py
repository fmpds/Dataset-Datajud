from fastapi import FastAPI
from datajud.controllers.import_process import ImportProcessController
from datajud.config import Settings
from datajud.database import engine
from datajud.routers import predict


settings = Settings()
app = FastAPI()

app.include_router(predict.router)

import_process_controller = ImportProcessController(app, engine)
