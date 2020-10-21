import pandas as pd
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from Util.PreProcess import SplitData

df = pd.read_csv(r"C:\Users\Romar\Google Drive\Master\DE\DE-group-5\Assignment 2\Data\data.csv")
X_train, X_test, y_train, y_test = SplitData(df)
# print(X_train)

clf = LinearRegression(n_jobs=-1)
clf.fit(X_train,y_train)
print('Train score: ' + str(clf.score(X_train, y_train)))
print('Test score: ' + str(clf.score(X_test, y_test)))
