from flask import Flask
import data
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/')
def get_data():
    df = data.load_data()
    filtered_data = data.filter_data(df)
    return filtered_data.to_json()