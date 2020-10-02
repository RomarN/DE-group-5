import json
import pandas as pd
from flask import Flask, json, request, Response
import os

#from resources import predictor

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/prediction/<model>', methods=['POST'])
def forest_fire_prediction(model):

    if model == "SVM":
        content = request.get_json()
        df = pd.read_json(json.dumps(content), orient='records') 
        # orient = Indication of expected JSON string format
        # E.g. records is like this: [{column -> value}, ... , {column -> value}]
              
        # Check if model repo exists on server
        model_repo = os.environ['MODEL_REPO']

        if model_repo:
            file_path = os.path.join(model_repo, "model.sav")
            model = load_model(file_path)

            # welke functies heeft model.sav?
            result = model.predict(df)

            # Wat krijg ik terug?
            result_dict = result.to_dict(orient='records')

            # return prediction result
            return json.dumps(result_dict, sort_keys=False, indent=4)

    elif model == "test":
        # Hardcoded test (source: PlotResults van ML assignment)
        result = [0.86611321, 0.43659247, 0.85455582, 1.95275274, 0.89050911]
        result_dict = result.to_dict(orient='records')
        return json.dumps(result_dict, sort_keys=False, indent=4)

    else:
        return json.dumps({'message': 'No model found.'}, sort_keys=False, indent=4)


app.run(host='0.0.0.0', port=5000)
