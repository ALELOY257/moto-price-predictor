from flask import Flask, request, jsonify
from joblib import load
import pandas as pd

model = load('precios_suzuki.pkl')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        features = [
                data.get("displacement"),
                data.get("compression"),
                data.get("bore"),
                data.get("stroke"),
                data.get("power"),
                data.get("torque"),
                data.get("engine"),
                data.get("fuel_system"),
                data.get("cooling"),
                data.get("front_suspension")
            ]
        
        if None in features:
            return jsonify({"error": "Missing data"}), 400
        
        fts_names = ['displacement', 'compression', 'bore', 'stroke', 'power', 'torque', 'engine', 'fuel_system', 'cooling', 'front_suspension']
        input_data = pd.DataFrame([features], columns=fts_names)

        prediction = model.predict(input_data)

        return jsonify({"Prediccion de precio": prediction[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)