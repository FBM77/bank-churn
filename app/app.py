from flask import Flask, request, jsonify
import pickle
import numpy as np
import sklearn  
from flask_cors import CORS, cross_origin  # type: ignore

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Charger le modèle et le scaler
with open('model/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    data = request.get_json()

    # Prétraitement des données d'entrée
    features = np.array([
        data["CreditScore"],
        data["Age"],
        data["Tenure"],
        data["Balance"],
        data["NumOfProducts"],
        data["HasCrCard"],
        data["IsActiveMember"],
        data["EstimatedSalary"],
        data["Satisfaction Score"],
        data["Point Earned"],
        data["Geography_France"],
        data["Geography_Germany"],
        data["Geography_Spain"],
        data["Gender_Female"],
        data["Gender_Male"],
        data["Card Type_DIAMOND"],
        data["Card Type_GOLD"],
        data["Card Type_PLATINUM"],
        data["Card Type_SILVER"]
    ]).reshape(1, -1)

    # Normalisation des données
    features_scaled = scaler.transform(features)

    # Prédiction avec le modèle chargé
    prediction = model.predict(features_scaled)[0]

    return jsonify({"prediction": int(prediction)})

if __name__ == '__main__':
    app.run(debug=False)