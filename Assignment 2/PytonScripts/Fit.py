import pandas as pd
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from Util.PreProcess import SplitData
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\Romar\Google Drive\Master\DE\DE-group-5\Assignment 2\Data\data.csv")
X_train, X_test, y_train, y_test = SplitData(df)
# print(X_train)

clf = LinearRegression(n_jobs=-1)
clf.fit(X_train, y_train)
print('Train score: ' + str(clf.score(X_train, y_train)))
print('Test score: ' + str(clf.score(X_test, y_test)))
print(len(y_test))


# plot 100 examples
y_pred = clf.predict(X_test)
x = list(range(99))
plt.figure(figsize=(5,3))
plt.plot(x,y_test[0:99], label = 'Actual values')
plt.plot(x,y_pred[0:99], label = 'Predicted values')
plt.ylim(0,100)
plt.legend()
plt.show()
