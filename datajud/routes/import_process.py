from fastapi import APIRouter
from datajud.controllers.import_process import ImportProcessController

router = APIRouter(prefix="/import", tags=["import"])

@router.get("/")
async def import_process(data: dict):
    import_process_controller = ImportProcessController()
    return import_process_controller.import_process()