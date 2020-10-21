import pandas as pd

from Util.PreProcess import SplitData

df = pd.read_csv(r"C:\Users\Romar\Google Drive\Master\DE\DE-group-5\Assignment 2\Data\data.csv")
X_train, X_test, y_train, y_test = SplitData(df)
print(X_test)

