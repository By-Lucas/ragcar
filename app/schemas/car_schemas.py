from typing import List
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class VehicleResult(BaseModel):
    marca: str
    modelo: str
    ano: int
    preco: float
    quilometragem: int


class QueryResponse(BaseModel):
    results: List[VehicleResult]
