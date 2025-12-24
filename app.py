from flask import Flask, request, render_template, jsonify
import h5py
import pickle
import numpy as np
import pandas as pd
from joblib import load
import requests

# Firebase Firestore REST API Endpoint
FIRESTORE_URL_TEMPLATE = "https://firestore.googleapis.com/v1/projects/heart-disease-smvitm/databases/(default)/documents/manual_predictions"
FIRESTORE_DOCUMENT_URL_TEMPLATE = FIRESTORE_URL_TEMPLATE + "/{email}"

# Load the model and scaler
def load_model_and_scaler(h5_file, scaler_file):
    with h5py.File(h5_file, 'r') as h5f:
        model_serialized = h5f['model'][()]
        model = pickle.loads(model_serialized.tobytes())
    
    scaler = load(scaler_file)
    return model, scaler

model, scaler = load_model_and_scaler('finall_model.h5', 'scaler (1).pkl')

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload_and_predict():
    if request.method == 'GET':
        return render_template('predict.html')
    elif request.method == 'POST':
        try:
            if request.form.get('age') and request.form.get('email') and request.form.get('name'):
                # Manual Prediction Logic
                input_data = np.array([[ 
                    float(request.form['age']),
                    float(request.form['sex']),
                    float(request.form['cp']),
                    float(request.form['trestbps']),
                    float(request.form['chol']),
                    float(request.form['fbs']),
                    float(request.form['restecg']),
                    float(request.form['thalach']),
                    float(request.form['exang']),
                    float(request.form['oldpeak']),
                    float(request.form['slope']),
                    float(request.form['ca']),
                    float(request.form['thal'])
                ]])

                # Scale input data
                input_data_scaled = scaler.transform(input_data)

                # Perform prediction
                prediction = model.predict(input_data_scaled)
                result = "Yes" if prediction[0] > 0.5 else "No"

                # Firestore document ID using email
                email = request.form['email']
                firestore_url = FIRESTORE_DOCUMENT_URL_TEMPLATE.format(email=email)

                # Prepare Firestore data
                firestore_data = {
                    "fields": {
                        "name": {"stringValue": request.form['name']},
                        "email": {"stringValue": email},
                        "age": {"integerValue": int(request.form['age'])},
                        "sex": {"stringValue": request.form['sex']},
                        "cp": {"integerValue": int(request.form['cp'])},
                        "trestbps": {"integerValue": int(request.form['trestbps'])},
                        "chol": {"integerValue": int(request.form['chol'])},
                        "fbs": {"stringValue": request.form['fbs']},
                        "restecg": {"integerValue": int(request.form['restecg'])},
                        "thalach": {"integerValue": int(request.form['thalach'])},
                        "exang": {"stringValue": request.form['exang']},
                        "oldpeak": {"doubleValue": float(request.form['oldpeak'])},
                        "slope": {"integerValue": int(request.form['slope'])},
                        "ca": {"integerValue": int(request.form['ca'])},
                        "thal": {"integerValue": int(request.form['thal'])},
                        "result": {"stringValue": result}
                    }
                }

                # Send data to Firestore
                response = requests.patch(firestore_url, json=firestore_data)
                if response.status_code == 200:
                    print("Prediction saved successfully to Firestore.")
                else:
                    print(f"Error saving to Firestore: {response.text}")

                return render_template('result.html', result=result)

            # CSV Prediction Logic (No Firestore)
            file = request.files.get('file')
            if file:
                data = pd.read_csv(file)

                # Drop the target column if it exists
                if 'target' in data.columns:
                    data = data.drop(columns=['target'])

                # Scale the data
                data_scaled = scaler.transform(data)

                # Make predictions
                predictions = model.predict(data_scaled)
                data['Prediction'] = ["Yes" if pred > 0.5 else "No" for pred in predictions]

                # Generate an HTML table for display
                result_table = data.to_html(classes='table table-bordered table-striped table-hover table-responsive', index=False)
                return render_template('result.html', table=result_table)

        except Exception as e:
            return render_template('result.html', error=f"Error: {str(e)}")

@app.route('/manual-predictions')
def manual_predictions():
    try:
        # Fetch all manual predictions from Firestore
        response = requests.get(FIRESTORE_URL_TEMPLATE)
        if response.status_code == 200:
            documents = response.json().get("documents", [])
            predictions = []
            for doc in documents:
                fields = doc["fields"]
                prediction = {
                    "name": fields.get("name", {}).get("stringValue", "N/A"),
                    "email": fields.get("email", {}).get("stringValue", "N/A"),
                    "age": fields.get("age", {}).get("integerValue", "N/A"),
                    "sex": fields.get("sex", {}).get("stringValue", "N/A"),
                    "cp": fields.get("cp", {}).get("integerValue", "N/A"),
                    "trestbps": fields.get("trestbps", {}).get("integerValue", "N/A"),
                    "chol": fields.get("chol", {}).get("integerValue", "N/A"),
                    "fbs": fields.get("fbs", {}).get("stringValue", "N/A"),
                    "restecg": fields.get("restecg", {}).get("integerValue", "N/A"),
                    "thalach": fields.get("thalach", {}).get("integerValue", "N/A"),
                    "exang": fields.get("exang", {}).get("stringValue", "N/A"),
                    "oldpeak": fields.get("oldpeak", {}).get("doubleValue", "N/A"),
                    "slope": fields.get("slope", {}).get("integerValue", "N/A"),
                    "ca": fields.get("ca", {}).get("integerValue", "N/A"),
                    "thal": fields.get("thal", {}).get("integerValue", "N/A"),
                    "result": fields.get("result", {}).get("stringValue", "N/A"),
                }
                predictions.append(prediction)
            return render_template('manual_predictions.html', predictions=predictions)
        else:
            return f"Error fetching predictions: {response.text}", 500
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
