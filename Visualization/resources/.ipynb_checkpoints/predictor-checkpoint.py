import json
import os

from keras.models import load_model


# make prediction
def predict(dataset):
    model_repo = os.environ['MODEL_REPO']
    if model_repo:
        file_path = os.path.join(model_repo, "model.h5")
        model = load_model(file_path)
        val_set2 = dataset.copy()
        result = model.predict(dataset)
        y_classes = result.argmax(axis=-1)
        val_set2['class'] = y_classes.tolist()
        dic = val_set2.to_dict(orient='records')
        return json.dumps(dic, indent=4, sort_keys=False)
    else:
        return json.dumps({'message': 'A model cannot be found.'},
                          sort_keys=False, indent=4)
