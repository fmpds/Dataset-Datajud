import os
from fastapi import FastAPI
from alembic.config import Config
from alembic import command
import pandas as pd

class ImportProcessController:
    def __init__(self, app: FastAPI, engine):
        app.on_event("startup")(self.startup_event)
        self.engine = engine

    async def startup_event(self):
        print("Starting up...")
        # Run Alembic migrations
        try: 
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
        except Exception as e:
            print(f"Error during Alembic migration: {e}")

        try: 
            # df = pd.read_csv("data.csv")
            # df.to_sql("data", con=self.engine, if_exists="replace")
            print("Data imported successfully")
        except Exception as e:
            print(f"Error during data import: {e}")

    def import_process(self):
        return {"message": "Hello World"}

