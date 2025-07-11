import pandas as pd
import random
import json
import os

# Leer el archivo CSV
df = pd.read_csv('static/hotel_bookings.csv')

# Filtrar filas canceladas y check-out
cancelled = df[df['is_canceled'] == 1].sample(n=10, random_state=42)
checkout = df[df['is_canceled'] == 0].sample(n=10, random_state=42)

# Mapeo de nombres y formato deseado
def traducir_fila(fila):
    return {
        "hotel": fila["hotel"],
        "comida": fila["meal"],
        "pais": fila["country"],
        "segmento_mercado": fila["market_segment"],
        "canal_distribucion": fila["distribution_channel"],
        "tipo_habitacion_reservada": fila["reserved_room_type"],
        "tipo_habitacion_asignada": fila["assigned_room_type"],
        "tipo_deposito": fila["deposit_type"],
        "tipo_cliente": fila["customer_type"],
        "mes_fecha_llegada": fila["arrival_date_month"],
        "tiempo_espera": int(fila["lead_time"]),
        "ano_fecha_llegada": int(fila["arrival_date_year"]),
        "numero_semana_fecha_llegada": int(fila["arrival_date_week_number"]),
        "dia_del_mes_fecha_llegada": int(fila["arrival_date_day_of_month"]),
        "estancias_noches_fin_semana": int(fila["stays_in_weekend_nights"]),
        "estancias_noches_semana": int(fila["stays_in_week_nights"]),
        "adultos": int(fila["adults"]),
        "ninos": int(fila["children"]),
        "bebes": int(fila["babies"]),
        "es_huesped_repetido": int(fila["is_repeated_guest"]),
        "cancelaciones_previas": int(fila["previous_cancellations"]),
        "reservas_anteriores_no_canceladas": int(fila["previous_bookings_not_canceled"]),
        "cambios_reserva": int(fila["booking_changes"]),
        "dias_en_lista_espera": int(fila["days_in_waiting_list"]),
        "tarifa_diaria_promedio": float(fila["adr"]),
        "plazas_aparcamiento_solicitadas": int(fila["required_car_parking_spaces"]),
        "total_solicitudes_especiales": int(fila["total_of_special_requests"])
    }

# Crear carpeta de salida si no existe
os.makedirs("samples", exist_ok=True)

# Guardar JSONs cancelados
for idx, (_, fila) in enumerate(cancelled.iterrows(), 1):
    salida = traducir_fila(fila)
    with open(f"samples/cancelled {idx}.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False)

# Guardar JSONs check-out
for idx, (_, fila) in enumerate(checkout.iterrows(), 1):
    salida = traducir_fila(fila)
    with open(f"samples/check-out {idx}.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False)

print("✅ Archivos generados en la carpeta 'jsons_salida'")
