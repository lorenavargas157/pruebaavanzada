# services.py
from database import get_db_connection, release_db_connection


# Cálculo de Energía Activa (EA)
def calculate_EA(connection, month):
    cursor = connection.cursor()

    # Sumar los valores de consumo para el mes, usando JOIN con records
    query_consumption = """
    SELECT SUM(consumption.value) 
    FROM consumption
    JOIN records ON consumption.id_record = records.id_record
    WHERE EXTRACT(MONTH FROM records.record_timestamp) = %s;
    """
    cursor.execute(query_consumption, (month,))
    consumption_sum = cursor.fetchone()[0]

    # Obtener la tarifa CU
    query_tariff = "SELECT CU FROM tariffs LIMIT 1;"
    cursor.execute(query_tariff)
    cu_tariff = cursor.fetchone()[0]

    # Calcular EA
    EA = consumption_sum * cu_tariff if consumption_sum else 0
    cursor.close()
    return EA

# Cálculo de Comercialización de Excedentes de Energía (EC)
def calculate_EC(connection, month):
    cursor = connection.cursor()

    # Sumar los valores de inyección para el mes, usando JOIN con records
    query_injection = """
    SELECT SUM(injection.value) 
    FROM injection
    JOIN records ON injection.id_record = records.id_record
    WHERE EXTRACT(MONTH FROM records.record_timestamp) = %s;
    """
    cursor.execute(query_injection, (month,))
    injection_sum = cursor.fetchone()[0]

    # Obtener la tarifa C
    query_tariff = "SELECT C FROM tariffs LIMIT 1;"
    cursor.execute(query_tariff)
    c_tariff = cursor.fetchone()[0]

    # Calcular EC
    EC = injection_sum * c_tariff if injection_sum else 0
    cursor.close()
    return EC

# Cálculo de Excedentes de Energía Tipo 1 (EE1)
def calculate_EE1(connection, month):
    cursor = connection.cursor()

    # Obtener la sumatoria de valores de inyección y consumo, usando JOIN con records
    query_injection = """
    SELECT SUM(injection.value) 
    FROM injection
    JOIN records ON injection.id_record = records.id_record
    WHERE EXTRACT(MONTH FROM records.record_timestamp) = %s;
    """
    cursor.execute(query_injection, (month,))
    injection_sum = cursor.fetchone()[0]

    query_consumption = """
    SELECT SUM(consumption.value) 
    FROM consumption
    JOIN records ON consumption.id_record = records.id_record
    WHERE EXTRACT(MONTH FROM records.record_timestamp) = %s;
    """
    cursor.execute(query_consumption, (month,))
    consumption_sum = cursor.fetchone()[0]

    # Obtener la tarifa CU negativa
    query_tariff = "SELECT CU FROM tariffs LIMIT 1;"
    cursor.execute(query_tariff)
    cu_tariff = cursor.fetchone()[0]
    cu_tariff_negative = -cu_tariff  # CU negativo

    # Determinar cantidad de EE1
    if injection_sum <= consumption_sum:
        EE1_amount = injection_sum
    else:
        EE1_amount = consumption_sum

    # Calcular EE1
    EE1 = EE1_amount * cu_tariff_negative if EE1_amount else 0
    cursor.close()
    return EE1

# Cálculo de Excedentes de Energía Tipo 2 (EE2)
def calculate_EE2(connection, month):
    cursor = connection.cursor()

    # Obtener la sumatoria de valores de inyección y consumo, usando JOIN con records
    query_injection = """
    SELECT SUM(injection.value) 
    FROM injection
    JOIN records ON injection.id_record = records.id_record
    WHERE EXTRACT(MONTH FROM records.record_timestamp) = %s;
    """
    cursor.execute(query_injection, (month,))
    injection_sum = cursor.fetchone()[0]

    query_consumption = """
    SELECT SUM(consumption.value) 
    FROM consumption
    JOIN records ON consumption.id_record = records.id_record
    WHERE EXTRACT(MONTH FROM records.record_timestamp) = %s;
    """
    cursor.execute(query_consumption, (month,))
    consumption_sum = cursor.fetchone()[0]

    # Determinar la cantidad de EE2
    if injection_sum <= consumption_sum:
        EE2 = 0  # No hay excedente tipo 2
    else:
        excess_energy = injection_sum - consumption_sum

        # Obtener tarifas hora a hora para los excedentes de energía
        query_hourly_data = """
        SELECT value 
        FROM xm_data_hourly_per_agent 
        WHERE EXTRACT(MONTH FROM record_timestamp) = %s;
        """
        cursor.execute(query_hourly_data, (month,))
        hourly_tariffs = cursor.fetchall()

        # Calcular EE2 usando la tarifa por hora
        EE2 = sum(hourly_value[0] for hourly_value in hourly_tariffs) * excess_energy

    cursor.close()
    return EE2

# Función para calcular la factura de energía completa
def calculate_energy_bill(connection, month):
    EA = calculate_EA(connection, month)
    EC = calculate_EC(connection, month)
    EE1 = calculate_EE1(connection, month)
    EE2 = calculate_EE2(connection, month)

    return {
        "Energía Activa (EA)": EA,
        "Comercialización Excedentes (EC)": EC,
        "Excedentes Tipo 1 (EE1)": EE1,
        "Excedentes Tipo 2 (EE2)": EE2
    }
