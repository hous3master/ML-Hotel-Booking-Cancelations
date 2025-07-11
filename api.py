from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model and preprocessing steps
with open('static/best_xgb_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('static/onehot_encoder.pkl', 'rb') as f:
    onehot = pickle.load(f)
with open('static/ordinal_encoder.pkl', 'rb') as f:
    ordinal = pickle.load(f)
with open('static/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Define columns used in transformation (must match training phase)
onehot_columns = ['hotel','comida','pais','segmento_mercado','canal_distribucion',
                  'tipo_habitacion_reservada','tipo_habitacion_asignada','tipo_deposito','tipo_cliente']
ordinal_columns = ['mes_fecha_llegada']
numeric_columns = ['tiempo_espera','ano_fecha_llegada','numero_semana_fecha_llegada',
                   'dia_del_mes_fecha_llegada','estancias_noches_fin_semana','estancias_noches_semana',
                   'adultos','ninos','bebes','es_huesped_repetido','cancelaciones_previas',
                   'reservas_anteriores_no_canceladas','cambios_reserva','dias_en_lista_espera',
                   'tarifa_diaria_promedio','plazas_aparcamiento_solicitadas','total_solicitudes_especiales']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Step 1: Parse input data
        input_data = request.get_json()
        df = pd.DataFrame([input_data])

        # Step 2: Apply transformations
        df_onehot = pd.DataFrame(onehot.transform(df[onehot_columns]),
                                 columns=onehot.get_feature_names_out(onehot_columns))
        df_ordinal = pd.DataFrame(ordinal.transform(df[ordinal_columns]), columns=ordinal_columns)
        df_scaled = pd.DataFrame(scaler.transform(df[numeric_columns]), columns=numeric_columns)

        # Step 3: Combine features
        df_final = pd.concat([df_onehot, df_ordinal, df_scaled], axis=1)

        # Step 4: Predict
        prediction = model.predict(df_final)[0]

        return jsonify({'prediction': int(prediction)})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)