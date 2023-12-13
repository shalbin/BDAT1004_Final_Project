from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import json

app = Flask(__name__)

# Route for index.html (Home Page)
@app.route('/')
def index():
    return render_template('/index.html')

# Generic route for each product request
@app.route('/google-charts/<stockname>')
def google_time_series(stockname):

    # Connecting to cloud database (MongoDb)
    client = MongoClient("mongodb+srv://shalbin13:hE9iW1z6vfM9ieva@cluster0.v4etain.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database('StockDB')
    records = db[stockname]
    
    # Getting the latest record
    for x in records.find():
        data = x

    data = data['values']

    custom_data = {'Datetime' : 'Closing value'}
    for x in reversed(data):  # Reverse the order of data
        custom_data[x['datetime']] = float(x['close'])

    return render_template('/time-series.html', data=custom_data, title=stockname)


if __name__ == "__main__":
    app.run()