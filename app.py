import pickle
import numpy as np
import pandas as pd
import json
from flask import Flask, request, render_template

import os

from geopy.geocoders import Nominatim # convert an address into latitude and longitude values


# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

# register for google maps API
GOOGLE_KEY = os.environ['GOOGLE_KEY']

app = Flask(__name__)
pipe = pickle.load(open('model/pipe.pkl', 'rb'))

df = pd.read_csv('data_final.csv')

# hospital lat lng
def hospital_loc():
    hospitals = [
        [43.659926, -79.388104, 'Toronto General Hospital'],
        [43.654287, -79.405273, 'Toronto Western Hospital']
        ]
    hospitals2 = json.dumps(hospitals)
    return hospitals2


# adding favicon
@app.route('/logo.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),'logo.ico', mimetype='image/png')

@app.route('/')
def hello():
    google_key = GOOGLE_KEY
    return render_template('patiently_waiting.html', google_key=google_key)

@app.route('/page')
def page():
    return render_template('toronto_walks.html')

@app.route('/stylebyarea', methods=['POST', 'GET'])
def stylebyarea():
    return render_template('predominant_styles_by_neighbourhood.html')

@app.route('/discover', methods=['POST', 'GET'])
def discover():
    return render_template('discover.html')

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')


@app.route('/result', methods=['POST','GET'])
def result(): # filename (/result is URL ending)
    if request.method == 'POST':
        # read inputs from form
        result = request.form
        # edit to update drop point
        starting_lat = float('43.647273') #  result.get('latitude'))
        starting_long = float('-79.386560') # result.get('longitude'))

        # predicts time
        new = pd.DataFrame({
            'Key': 201908,
            'day':[result.get('day')],
            'Org_ID': 1364, # [result.get('Org_ID')],
            'WaitTime_90percentile': 3.2, #[result.get('WaitTime_90percentile')],
            'case_per_day': 1183,
            'case_per_month': 4942 #[result.get('number_of_cases')]
        })
    prediction_time = pipe.predict(new)[0]

    # hospital closest to that wait time
    index = abs(df['WaitTime_mean'] - prediction_time).idxmin()
    hospital = df.iloc[index,1]

    hospitals2 = hospital_loc()

    # map display
    google_key = GOOGLE_KEY

    return render_template('result.html', prediction_time=prediction_time, hospital=hospital, starting_lat=starting_lat, starting_long=starting_long, hospitals=hospitals2, google_key=google_key)


if __name__ == '__main__':
    app.run(debug=True, port=8000) #(debug=True) --> remove this when everything has been built
