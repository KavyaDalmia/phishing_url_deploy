from flask import Flask, render_template, request
import pickle
from features_extraction import *
import numpy as np
from flask import Flask, request, redirect, url_for, render_template, flash
#import pytesseract
from PIL import Image
import os
import requests
import json
import re

from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')

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
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = 'supersecretkey'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load your pickle model
with open('NeuralNetwork.pickle.dat', 'rb') as f:
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
    try:
        rounded_prediction = round(prediction[0][0])
    except:
        rounded_prediction = 1
        
    print(prediction[0][0])
    print("Rounded Prediction:", rounded_prediction)
    # Render a template with the prediction
    if rounded_prediction == 1:
        final_prediction = 'PHISHING! DO NOT FALL FOR IT, DONT CLICK ON IT'
    elif rounded_prediction == 0:
        final_prediction = 'Safe url'
    return render_template('result.html', extracted_text=None, prediction=final_prediction)


# Define a route to handle image upload form submission
@app.route('/upload', methods=['POST']) #the /upload willl trigger upload_file func that accepts only POST requests
def upload_file():
    if 'file' not in request.files:
        flash('No file part') #flash meassage for the user
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(filepath)
        file.save(filepath)
        url = extract_text_from_image(filepath)
        #print('found a url' + url)
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
        return render_template('result.html', extracted_text=url, prediction=final_prediction)

        #return render_template('result.html', extracted_text=text, prediction=None)

def extract_text_from_image(image_path):
    api_url = 'https://api.api-ninjas.com/v1/imagetotext'
    headers = {'X-Api-Key': api_key}
    image_file_descriptor = open(image_path, 'rb')
    files = {'image': image_file_descriptor}
    r = requests.post(api_url, files=files, headers=headers)
    data = (r.json())
    text_fields = [item["text"] for item in data]
    url_pattern = r"(?:https?://|www\.)\S+|(?<=\s)[\w-]+\.[\w.-]+"
    # Search for URLs in the strings list
    urls_found = [string for string in text_fields if re.search(url_pattern, string)]
    print(urls_found)
    if urls_found:
        print('extract func' + urls_found[0])
        extracted_text = urls_found[0]
    else:
        extracted_text = 'No urls found'
    
    return extracted_text

# def look_for_urls(strings_list):
#     # Define a regex pattern for matching URLs
#     url_pattern = r"(?:https?://|www\.)\S+|(?<=\s)[\w-]+\.[\w.-]+"
#     # Search for URLs in the strings list
#     urls_found = [string for string in strings_list if re.search(url_pattern, string)]
#     print(urls_found)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
