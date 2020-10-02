import json
import os

from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score,cross_val_predict


def predict_svm(dataset):
    clf = SVR(kernel ='rbf', gamma = 1.2, C = 1.4, epsilon=0.1)
    clf.fit(X_train,y_train)
    y_pred_SVM = clf.predict(X_test)
    
    dic = vy_pred_SVM.to_dict(orient='records')
    return json.dumps(dic, indent=4, sort_keys=False)

# from keras.models import load_model
#
# # make prediction
# def predict(dataset):
#     model_repo = os.environ['MODEL_REPO']
#     if model_repo:
#         file_path = os.path.join(model_repo, "model.h5")
#         model = load_model(file_path)
#         val_set2 = dataset.copy()
#         result = model.predict(dataset)
#         y_classes = result.argmax(axis=-1)
#         val_set2['class'] = y_classes.tolist()
#         dic = val_set2.to_dict(orient='records')
#         return json.dumps(dic, indent=4, sort_keys=False)
#     else:
#         return json.dumps({'message': 'A model cannot be found.'},
#                           sort_keys=False, indent=4)
