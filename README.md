running the app

```bash
uvicorn main:app --reload
```

running the app with poetry

```bash
poetry install

poetry run uvicorn datajud.app:app --reload
```

running the app with docker

```bash
docker-compose up -d
```
