from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.car_models import CarModels


async def save_response_log(session:AsyncSession, query_text: str, response_data: dict):
    stmt = select(CarModels).where(CarModels.query_text == query_text)
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        print("Resposta já registrada no banco, não será duplicada.")
        return

    session.add(CarModels(
        query_text=query_text,
        response_data=response_data,
        filters_json={}
    ))
    await session.commit()