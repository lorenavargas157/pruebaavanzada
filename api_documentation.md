# API de Cálculo de Facturación de Energía

## Información General
- **Título**: API de Cálculo de Facturación de Energía
- **Versión**: 1.0.0
- **Descripción**: API RESTful desarrollada con FastAPI para calcular facturas de energía, estadísticas de clientes y carga del sistema.

## Endpoints

### POST /calculate-invoice
- **Resumen**: Calcula la factura para un cliente y un mes específico.
- **Descripción**: Este endpoint calcula los valores de la factura de energía para un mes específico.
- **Cuerpo de la solicitud**:
    ```json
    {
      "month": 1
    }
    ```
- **Respuesta**:
    - **Código 200**:
        ```json
        {
          "EA": 100,
          "EC": 50,
          "EE1": 20,
          "EE2": 30
        }
        ```
        - **Descripción**: Respuesta que incluye los cálculos de la factura.
        - **Esquema**: 
        ```json
        {
          "EA": 100,   // Energía activa (en kWh o unidades correspondientes)
          "EC": 50,    // Energía consumida (en kWh o unidades correspondientes)
          "EE1": 20,   // Energía de un primer concepto (en kWh o unidades correspondientes)
          "EE2": 30    // Energía de un segundo concepto (en kWh o unidades correspondientes)
        }
        ```
    - **Código 500**: Error en el servidor.

### GET /client-statistics/{client_id}
- **Resumen**: Proporciona estadísticas de consumo e inyección para un cliente.
- **Descripción**: Este endpoint devuelve las estadísticas de consumo e inyección para un cliente específico.
- **Parámetros**:
    - `client_id` (integer): ID del cliente.
- **Respuesta**:
    - **Código 200**:
        ```json
        {
          "total_consumption": 200,
          "total_injection": 150
        }
        ```
        - **Esquema**:
        ```json
        {
          "total_consumption": 200,   // Consumo total (en kWh o unidades correspondientes)
          "total_injection": 150       // Inyección total (en kWh o unidades correspondientes)
        }
        ```
    - **Código 404**: Cliente no encontrado.

### GET /system-load
- **Resumen**: Muestra la carga del sistema por hora basada en los datos de consumo.
- **Descripción**: Este endpoint devuelve la carga del sistema agrupada por hora.
- **Respuesta**:
    - **Código 200**:
        ```json
        [
          {"hour": 0, "load": 10},
          {"hour": 1, "load": 15}
        ]
        ```
        - **Esquema**:
        ```json
        {
          "hour": 0,    // Hora del día (0-23)
          "load": 10    // Carga total (en kWh o unidades correspondientes)
        }
        ```

### GET /calculate/concept/{concept}/{month}
  - **Resumen**: Calcula un concepto específico de la factura de energía para un mes determinado.
    - **EA (Energía Activa)**: La energía consumida durante el mes.
    - **EC (Comercialización de Excedentes de Energía)**: Energía excedente inyectada al sistema.
    - **EE1 (Excedentes de Energía tipo 1)**: Excedentes que no superan la energía consumida.
    - **EE2 (Excedentes de Energía tipo 2)**: Excedentes que superan la energía consumida, con cálculo hora a hora.

- **Descripción**: Este endpoint calcula un concepto energético específico (EA, EC, EE1 o EE2) para un mes determinado. Dependiendo del concepto, se aplican diferentes reglas y fórmulas para obtener los valores.

- **Parámetros**:
    - `concept` (string): Concepto a calcular (EA, EC, EE1, EE2).
    - `month` (integer): Mes para el cálculo.
- **Respuesta**:
    - **Código 200**:
        ```json
        {
          "EA": 100
        }
        ```
    - **Código 400**: Concepto no válido.

## Esquemas

### InvoiceRequest
```json
{
  "month": 1
}


{
  "EA": 100,   // Energía activa (en kWh o unidades correspondientes)
  "EC": 50,    // Energía consumida (en kWh o unidades correspondientes)
  "EE1": 20,   // Energía de un primer concepto (en kWh o unidades correspondientes)
  "EE2": 30    // Energía de un segundo concepto (en kWh o unidades correspondientes)
}
