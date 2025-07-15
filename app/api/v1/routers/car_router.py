import os
from typing import Annotated
from fastapi.params import Depends
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.car_schemas import QueryRequest
from app.utils.save_response import save_response_log
from app.services.vehicle_search import VehicleSearchService
from app.services.ingest_excel import ExcelPineconeIngestor


router = APIRouter(prefix="")


@router.post("/query")
async def query_vehicles(
    data: QueryRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    service = VehicleSearchService(data.query)
    raw_results = service.run()
    response = service.return_result(raw_results)

    await save_response_log(
        session=session,
        query_text=data.query,
        response_data=response,
    )

    return response


@router.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        ingestor = ExcelPineconeIngestor(excel_path=tmp_path)
        ingestor.run()
        return {"status": "ingestão de dados para o PINECONE concluída com sucesso"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.remove(tmp_path)


@router.get("/health")
async def health_check():
    return {"status": "ok"}
