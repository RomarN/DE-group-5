import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd

pd.options.mode.chained_assignment = None
from sklearn.model_selection import train_test_split
from category_encoders import TargetEncoder


# read the data uncomment to test
# df = pd.read_csv(r"C:\Users\Romar\Google Drive\Master\DE\DE-group-5\Assignment 2\Data\data.csv")


def PreprocessData(df):
    # Remove all NaN rows
    df_preprocessed = df.dropna()

    # one hot encoding nationality
    encoder = TargetEncoder()
    df_preprocessed['Nationality Encoded'] = encoder.fit_transform(df_preprocessed['Nationality'],
                                                                   df_preprocessed['Overall'])
    df_preprocessed.pop('Nationality')

    # one hot encoding club (remove NaN first)
    encoder = TargetEncoder()
    df_preprocessed['Club Encoded'] = encoder.fit_transform(df_preprocessed['Club'], df_preprocessed['Overall'])
    df_preprocessed.pop('Club')

    # onehot encoding preferred foot (remove NaN first)\
    encoder = TargetEncoder()
    df_preprocessed['Preferred Foot Encoded'] = encoder.fit_transform(df_preprocessed['Preferred Foot'],
                                                                      df_preprocessed['Overall'])
    df_preprocessed.pop('Preferred Foot')

    # encode Workrate
    encoder = TargetEncoder()
    df_preprocessed['Work Rate Encoded'] = encoder.fit_transform(df_preprocessed['Work Rate'],
                                                                 df_preprocessed['Overall'])
    df_preprocessed.pop('Work Rate')

    # encode BodyType
    encoder = TargetEncoder()
    df_preprocessed['Body Type Encoded'] = encoder.fit_transform(df_preprocessed['Body Type'],
                                                                 df_preprocessed['Overall'])
    df_preprocessed.pop('Body Type')

    # encode position
    encoder = TargetEncoder()
    df_preprocessed['Position Encoded'] = encoder.fit_transform(df_preprocessed['Position'], df_preprocessed['Overall'])
    df_preprocessed.pop('Position')

    # Value
    value = df_preprocessed.Value
    newvalue = []
    for ITEM in value:
        temp = ITEM.split("€")[1]
        if ITEM[-1] == 'K':
            newvalue.append(float(temp.split("K")[0]))
        elif ITEM[-1] == 'M':
            newvalue.append(float(temp.split("M")[0]))
        else:
            newvalue.append(float(temp))
    df_preprocessed['Value'] = newvalue
    newvalue = []

    # Wage
    wage = df_preprocessed.Wage
    newwage = []
    for ITEM in wage:
        temp = ITEM.split("€")[1]
        newwage.append(float(temp.split("K")[0]))
    df_preprocessed['Wage'] = newwage
    newwage = []

    # Weight
    weight = df_preprocessed.Weight
    newweight = []
    for ITEM in weight:
        newweight.append(float(ITEM.split("lbs")[0]))
    df_preprocessed['Weight'] = newweight
    newweight = []

    # Height
    newheight = []
    height = df_preprocessed.Height
    for ITEM in height:
        feet, inch = float(ITEM.split("'")[0]), float(ITEM.split("'")[1])
        newheight.append(feet * 30.48 + inch * 2.54)
    df_preprocessed['Height'] = newheight
    newheight = []

    # All the positions, weet niet wat we daar mee willlen
    positions = ['LS', 'ST', 'RS', 'LW', 'CF', 'RF', 'RW', 'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB',
                 'LDM', 'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']

    for position in positions:
        data = []
        new_data = []
        data = df_preprocessed[position]
        for ITEM in data:
            new_data.append(float(ITEM.split("+")[0]) + float(ITEM.split("+")[1]))
        df_preprocessed[position] = new_data
        new_data = []

    return df_preprocessed


def SplitData(df):
    # remove irrelevant columns
    df.pop('ID')
    df.pop('Unnamed: 0')
    df.pop('Photo')
    df.pop('Flag')
    df.pop('Club Logo')
    df.pop('Release Clause')
    df.pop('Name')
    df.pop('Loaned From')
    df.pop('Real Face')
    df.pop('Contract Valid Until')
    df.pop('Joined')

    # preprocess the dataframe
    df_pp = PreprocessData(df)

    # Create a train and test split
    y = df_pp.pop('Overall')
    X_train, X_test, y_train, y_test = train_test_split(df_pp, y, test_size=0.33, random_state=42)
    return X_train, X_test, y_train, y_test

# uncomment to test
# X_train, X_test, y_train, y_test = SplitData(df)
# print(X_train)
