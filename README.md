# HeartGuard AI - Heart Disease Prediction

HeartGuard AI is a web application designed to predict heart disease risk based on patient information. It uses a machine learning model to predict the likelihood of heart disease and allows users to make predictions via manual data entry or CSV file upload.

## Features

- **Manual Prediction:** Users can input patient details such as age, sex, blood pressure, cholesterol, and other relevant health metrics to get a heart disease risk prediction.
- **CSV File Prediction:** Users can upload a CSV file containing patient data, and the system will predict the risk of heart disease for each entry.
- **Data Storage:** Manual predictions are stored in Firebase Firestore, including patient details and prediction results. (No Firestore storage for CSV predictions.)
- **Admin View:** Admins can view all manually submitted predictions, with the ability to edit or delete records.

## Technologies Used

- **Flask:** For creating the web server and handling requests.
- **Scikit-learn:** For the machine learning model (SVM) and data scaling.
- **Firebase Firestore:** For storing manual prediction data.
- **Pandas & NumPy:** For data manipulation and processing.
- **H5Py & Joblib:** For saving and loading the trained model.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/heartguard-ai.git

2. Create a virtual environment:
```bash
python3 -m venv venv
```
   
3. Activate the virtual environment:
Windows:

 ```bash
.\venv\Scripts\activate
```
4. Requirements
```bash
pip install -r requirements.txt
```


Setup Firebase
Create a Firebase project if you don't already have one: https://console.firebase.google.com/
Set up Firestore in your Firebase project.
Obtain your Firebase configuration details and replace them in the appropriate section of the code (app.py).
Running the Application
To start the Flask application, run the following command:

bash
Copy code
python app.py
This will start the Flask development server on http://localhost:5000.

Usage
Manual Prediction: Go to the /predict page, enter patient details, and submit the form to get a prediction.
CSV Prediction: On the same page, upload a CSV file with patient data and submit it for batch predictions.
View Predictions: Admins can view all manual predictions at /manual-predictions.
Endpoints
POST /predict: Handles manual prediction submissions and stores them in Firestore.
GET /manual-predictions: Displays all manually submitted predictions.
POST /edit-prediction/<email>: Allows admins to edit a patient's data.
DELETE /delete-prediction/<email>: Allows admins to delete a patient's prediction record.
Firestore Data Structure
Manual prediction records are stored in Firestore with the following fields:

name: Patient's name
email: Patient's email (used as document ID)
age: Patient's age
sex: Patient's sex
cp: Chest pain type
trestbps: Resting blood pressure
chol: Cholesterol level
fbs: Fasting blood sugar
restecg: Resting ECG type
thalach: Maximum heart rate
exang: Exercise induced angina
oldpeak: ST depression induced by exercise
slope: Slope of peak exercise ST
ca: Number of major vessels colored by fluoroscopy
thal: Thalassemia
result: Heart disease risk prediction (Yes/No)
Contributing
Contributions are welcome! If you would like to improve this project, please feel free to submit a pull request.

License
This project is open-source and available under the MIT License.

About
Developed by: [Your Name or Organization]

markdown
Copy code

---

### Key Sections in the `README.md`:

1. **Project Overview:** Briefly explains the purpose and features of the project.
2. **Technologies Used:** Lists the major technologies and tools used in the project.
3. **Installation Instructions:** Provides step-by-step setup instructions.
4. **Setup Firebase:** A guide for setting up Firebase to store manual prediction data.
5. **Running the Application:** Explains how to start the Flask application.
6. **Usage Instructions:** Describes how to use the application, including manual and CSV predictions.
7. **Endpoints:** Provides a summary of API endpoints for managing predictions.
8. **Firestore Data Structure:** Details how the data is stored in Firestore.
9. **Contributing:** Encourages others to contribute to the project.
10. **License:** Provides license details (MIT license by default).

### Usage:
- The `README.md` file will help you or others easily set up and understand the project. You can mod