import json
import pandas as pd
from flask import Flask, json, request, Response
import os
import pickle

#from resources import predictor

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/prediction/<model>', methods=['POST'])
def forest_fire_prediction(model):

    if model == "SVM":
        content = request.get_json()
        df = pd.read_json(json.dumps(content), orient='records') 

        model_repo = os.environ['MODEL_REPO']
        file_path = os.path.join(model_repo, "model.sav")
        
        with open(file_path, "rb") as f:
            model = pickle.load(f)

            # Model returns list of predictions
            result = model.predict(df)

            # Transform list into dict          
            result_dict = { i : result[i] for i in range(0, len(result) ) }

            
        # Return prediction result as JSON   
        return json.dumps(result_dict, sort_keys=False, indent=4)

    else:
        return json.dumps({'message': 'No model found - DEBUGGING.PY'}, sort_keys=False, indent=4)


app.run(host='0.0.0.0', port=5003)
