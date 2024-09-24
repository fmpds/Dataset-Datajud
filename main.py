import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datajud.controllers.import_process import ImportProcessController

load_dotenv()

app = FastAPI()

database_uri = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(database_uri)

# Initialize the ImportProcessController
import_process_controller = ImportProcessController(app, engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/import")
async def import_process():
    return import_process_controller.import_process()