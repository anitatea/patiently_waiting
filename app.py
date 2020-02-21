import pickle
import numpy as np
import pandas as pd
import json
from flask import Flask, request, render_template

import os

from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

# comment out when uploading to Heroku
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

# google maps API
GOOGLE_KEY = os.environ['GOOGLE_KEY']

app = Flask(__name__)
pipe = pickle.load(open('model/pipe.pkl', 'rb'))

df = pd.read_csv('data_final.csv')


# hospital lat lng, name, id
def append_hospital_info(df_pred):
    hospital_loc = pd.DataFrame([
        [43.659926, -79.388104, 'Toronto General Hospital', 1359],
        [43.654287, -79.405273, 'Toronto Western Hospital', 1364],
        [43.658326, -79.390901, 'Mount Sinai Hospital', 3742],
        [43.640810, -79.450281, "St. Joseph's Hospital", 4800],
        [43.653202, -79.377691, "St. Michael's Hospital", 4831],
        [43.657507, -79.387604, 'The Hospital For Sick Children', 4824],
        [43.722779, -79.374001, 'Sunnybrook Health Sciences Centre', 4931],
        [43.691177, -79.325245, 'Michael Garron Hospital', 4935]
        ])
    hospital_loc = hospital_loc.rename(columns={3:"id"})

    # merge both dataframes & convert to json
    merged = pd.merge(hospital_loc, df_pred, on='id', how='outer')
    merged_list = merged.values.tolist()
    hosp_info = json.dumps(merged_list)
    return hosp_info

hospital_ids = [1364, 1359, 4935, 3742, 4824, 4931, 4800, 4831, 4850]

def predict_wait_times(day):
    pred = pd.DataFrame()
    for id in hospital_ids:
        # finds averages
        print(day)
        filtered = df.loc[(df['day'] == day) & (df['Org_ID'] == id)]
        avg_90percentile = filtered['WaitTime_90percentile'].sum()/len(filtered)
        avg_num_per_day = filtered['case_per_day'].sum()/len(filtered)
        print(avg_num_per_day)

        new = pd.DataFrame({
            'Key': 202002,
            'day':[day],
            'Org_ID': id, # [result.get('Org_ID')],
            'WaitTime_90percentile': avg_90percentile,
            'case_per_day': avg_num_per_day
        })
        # model and round to 2 decimal places
        row = [[id, '{:,.2f}'.format(pipe.predict(new)[0])]]
        pred = pred.append(row)

    # to be merged with hospital_loc
    pred = pred.rename(columns={0:'id'})
    return pred

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

@app.route('/cool_things', methods=['POST', 'GET'])
def cool_things():
    return render_template('cool_things.html')

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
        selected_day = result['day'] #.get('day')
        # output is [hospital_id, wait_time]
        df_pred = predict_wait_times(selected_day)

        # append hospital info together
        hospital_predictions = append_hospital_info(df_pred)

        # hospital closest to that wait time
        # index = abs(df['WaitTime_mean'] - prediction_time).idxmin()
        # hospital = df.iloc[index,1]

        # map display
        google_key = GOOGLE_KEY

        return render_template('result.html', hospital_predictions=hospital_predictions, day=selected_day, starting_lat=starting_lat, starting_long=starting_long, google_key=google_key)

if __name__ == '__main__':
    app.run(debug=True, port=8000) #(debug=True) --> remove this when everything has been built
