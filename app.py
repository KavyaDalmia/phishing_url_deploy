from flask import Flask, render_template, request
import pickle
from features_extraction import *
import numpy as np

feature_names = ['length', 'check_shortening','check_for_iframe', 'check_for_bar_manipulation','check_for_right_click_disabled', 'web_tracffic']
def featureExtraction2(url):
    features = []
    try:
        response = requests.get(url)
    except:
        response = ""
    features.append(length(url))
    features.append(check_shortening(url))
    features.append(check_for_iframe(response))
    features.append(check_for_bar_manipulation(response))
    features.append(check_for_right_click_disabled(response))
    features.append(web_traffic(url))
    return features

app = Flask(__name__)

# Load your pickle model
with open('NeuralNetwrok.pickle.dat', 'rb') as f:
    model = pickle.load(f)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route to handle form submission
@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from the form
    url = request.form['user_input']

    # Perform any processing on the input
    features = featureExtraction2(url)
    features_array = np.array(features, dtype=np.float32)  # Convert to float32 if needed
    input_data = np.array([features_array])
    # Use your model to generate predictions
    prediction = model.predict(input_data)
    print(features)
    rounded_prediction = round(prediction[0][0])
    print("Rounded Prediction:", rounded_prediction)
    # Render a template with the prediction
    if rounded_prediction == 1:
        final_prediction = 'PHISHING! DO NOT FALL FOR IT, DONT CLICK ON IT'
    elif rounded_prediction == 0:
        final_prediction = 'Safe url'
    return render_template('result.html', prediction=final_prediction)

if __name__ == '__main__':
    app.run(debug=True)
