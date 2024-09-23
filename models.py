# models.py
from pydantic import BaseModel

class InvoiceRequest(BaseModel):
    client_id: int
    month: int

class InvoiceResponse(BaseModel):
    EA: float
    EC: float
    EE1: float
    EE2: float

class StatisticsResponse(BaseModel):
    total_consumption: float
    total_injection: float

class SystemLoadResponse(BaseModel):
    hour: int
    load: float
