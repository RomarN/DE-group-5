import os
import pandas as pd
import requests
from flask import Flask, json, Response

from Resources.util import preprocess, read_data_records

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/training-dbpp/<table_name>', methods=['POST'])
def preprocess_table(table_name):
    db_api = os.environ['TRAIN_DB_API']
    r = requests.get(db_api)
    j = r.json()
    df = pd.DataFrame.from_dict(j)
    preprocess(df, table_name)
    return json.dumps({'message': 'pre-processing complete, table has been created'}, sort_keys=False, indent=4), 200

@app.route('/training-dbpp/<table_name>', methods=['GET'])
def read_data(table_name):
    df = read_data_records(table_name)
    df = df.drop(columns=['id'])
    resp = Response(df.to_json(orient='records'), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Max-Age'] = '1000'
    return resp

app.run(host='0.0.0.0', port=5000)