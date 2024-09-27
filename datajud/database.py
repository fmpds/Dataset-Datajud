from sqlalchemy.orm import declarative_base, sessionmaker
from datajud.config import Settings
from sqlalchemy import create_engine

settings = Settings()
print(settings)
database_uri = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(database_uri, echo=True)

SessionLocal = sessionmaker(
    engine, expire_on_commit=False
)

Base = declarative_base()
