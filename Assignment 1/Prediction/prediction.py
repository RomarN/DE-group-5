import json
import pandas as pd
from flask import Flask, json, request, Response
import os
import pickle
from  sklearn.svm import SVR

app = Flask(__name__)
app.config["DEBUG"] = True

RESULT = []

@app.route('/prediction/<model>', methods=['POST'])
def forest_fire_prediction(model):
    global RESULT

    if model == "SVM":
        content = request.get_json()
        df = pd.read_json(json.dumps(content), orient='records') 
        # orient = Indication of expected JSON string format
        # E.g. records is like this: [{column -> value}, ... , {column -> value}]
              
        # Check if model repo exists on server
        model_repo = os.environ['MODEL_REPO']

        if model_repo:

            file_path = os.path.join(model_repo, "model.sav")
            model = pickle.load(open(file_path, 'rb'))
            # Model returns list of predictions
            result = model.predict(df)
            RESULT = result
            # Transform list into dict          
            result_dict = { i : result[i] for i in range(0, len(result) ) }
            RESULT = result
            # Return prediction result as JSON
            return json.dumps(result_dict, sort_keys=False, indent=4)

    elif model == "test":
        # Hardcoded test (source: PlotResults van ML assignment)
        result = [0.86611321, 0.43659247, 0.85455582, 1.95275274, 0.89050911]
        result_dict = { i : result[i] for i in range(0, len(result) ) }
        return json.dumps(result_dict, sort_keys=False, indent=4)

    else:
        return json.dumps({'message': 'No model found.'}, sort_keys=False, indent=4)


@app.route('/prediction/db', methods=['GET'])
def send_data():
    global RESULT
    df_result = pd.DataFrame(RESULT, columns = ['area'])
    resp = Response(df_result.to_json(orient='records'), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Max-Age'] = '1000'
    return resp


app.run(host='0.0.0.0', port=5000)
