from sklearn.svm import SVR
import pandas as pd
import os
import json
import pickle


def preprocess(df):
    # Convert the categorical data into binary values
    df_bin = df.join(pd.get_dummies(df.pop('day')))
    df_bin = df_bin.join(pd.get_dummies(df_bin.pop('month')))
    df_bin.pop('sun')
    df_bin.pop('dec')
    # Return the database
    return df_bin



def model_trainer(df):
    df = preprocess(df)
    y = df.pop('area')
    X = df
    model = SVR()
    model.fit(X,y)
    score = model.score(X, y)

    # Saving model in a given location (provided as an env. variable
    model_repo = os.environ['MODEL_REPO']
    if model_repo:
        file_path = os.path.join(model_repo, "model.sav")
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
    else:
        pickle.dump(model, open('model.sav', 'wb'))
        return json.dumps({'message': 'The model was saved locally.'},
                          sort_keys=False, indent=4), 200

    print("Saved the model to disk")
    return json.dumps(score, sort_keys=False, indent=4)