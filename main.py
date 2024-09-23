# main.py
from fastapi import FastAPI, HTTPException
from models import InvoiceRequest, InvoiceResponse, StatisticsResponse, SystemLoadResponse
from services import calculate_EA, calculate_EC, calculate_EE1, calculate_EE2
from database import get_db_connection, release_db_connection

app = FastAPI()

@app.post("/calculate-invoice", response_model=InvoiceResponse)
def calculate_invoice(request: InvoiceRequest):
    month = request.month
    connection = get_db_connection()  

    try:
        EA = calculate_EA(connection, month) 
        EC = calculate_EC(connection, month)
        EE1 = calculate_EE1(connection, month)
        EE2 = calculate_EE2(connection, month)

        return {
            "EA": EA,
            "EC": EC,
            "EE1": EE1,
            "EE2": EE2
        }
    finally:
        release_db_connection(connection)  


@app.get("/client-statistics/{client_id}", response_model=StatisticsResponse)
def get_client_statistics(client_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Obtener estadísticas de consumo
    query_consumption = """
    SELECT SUM(consumption.value)
    FROM consumption
    JOIN records ON consumption.id_record = records.id_record
    WHERE records.id_service = %s;
    """
    cursor.execute(query_consumption, (client_id,))
    total_consumption = cursor.fetchone()[0] or 0

    # Obtener estadísticas de inyección
    query_injection = """
    SELECT SUM(injection.value)
    FROM injection
    JOIN records ON injection.id_record = records.id_record
    WHERE records.id_service = %s;
    """
    cursor.execute(query_injection, (client_id,))
    total_injection = cursor.fetchone()[0] or 0

    cursor.close()
    release_db_connection(connection)

    return {
        "total_consumption": total_consumption,
        "total_injection": total_injection
    }

@app.get("/system-load", response_model=list[SystemLoadResponse])
def get_system_load():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT EXTRACT(HOUR FROM records.record_timestamp) AS hour, SUM(consumption.value) AS load
    FROM consumption
    JOIN records ON consumption.id_record = records.id_record
    GROUP BY hour
    ORDER BY hour;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    release_db_connection(connection)

    return [{"hour": int(row[0]), "load": row[1]} for row in results]

# Endpoint para cada concepto
@app.get("/calculate/concept/{concept}/{month}")
def calculate_concept(concept: str, month: int):
    connection = get_db_connection()  
    try:
        if concept == "EA":
            return {"EA": calculate_EA(connection, month)}  
        elif concept == "EC":
            return {"EC": calculate_EC(connection, month)}  
        elif concept == "EE1":
            return {"EE1": calculate_EE1(connection, month)}  
        elif concept == "EE2":
            return {"EE2": calculate_EE2(connection, month)}  
        else:
            raise HTTPException(status_code=400, detail="Concepto no válido")
    finally:
        release_db_connection(connection)  

