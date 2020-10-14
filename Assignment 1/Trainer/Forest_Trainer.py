import os
import pandas as pd
import requests
from flask import Flask, json, Response

from Resources.Trainer_utilities import model_trainer

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/training-cp/<model>', methods=['POST'])
def train_models(model):
    db_api = os.environ['PREPROCESS_DB_API']
    r = requests.get(db_api)
    j = r.json()
    df = pd.DataFrame.from_dict(j)
    if model == "fire":
        js = model_trainer(df)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Max-Age'] = '1000'
        return resp
    else:
        return json.dumps({'message': 'the given model is not supported dropped'},
                          sort_keys=False, indent=4), 400


app.run(host='0.0.0.0', port=5000)
