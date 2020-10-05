import pandas as pd
from flask import Flask, json, request, Response

from resources import predictor

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/prediction-cp/<model>', methods=['POST'])
def predict_perf(model):
    content = request.get_json()
    df = pd.read_json(json.dumps(content), orient='records')
    if model == "mlp":
        js = predictor.predict(df)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Max-Age'] = '1000'
        return resp
    else:
        return json.dumps({'message': 'the given model is not supported dropped'},
                          sort_keys=False, indent=4), 400


app.run(host='0.0.0.0', port=5000)
