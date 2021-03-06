from flask import Flask, render_template
import base64
from io import BytesIO
# from matplotlib.figure import Figure

import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from google.cloud import storage
import pickle

app = Flask(__name__, static_folder="templates")
app.config["DEBUG"] = True


@app.route('/visualize')
def index():
    project_id = 'weighty-flag-288919'
    bucket_name = 'delabs2020'
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('predictions/predictions.csv')
    blob.download_to_filename('download.csv')


    # Load necessary data
    results = pd.read_csv('download.csv')

    # Generate the figure **without using pyplot**.
    # line 1 points
    plt.figure(figsize=(20, 10))
    x = results['date']
    dates = []
    for item in x:
        temp = str(item)
        dates.append(temp[5:])
    y1 = results['predictions']
    y2 = results['actual']
    # plotting the line 1 points
    plt.plot(dates, y1, label="predictions")

    # plotting the line 2 points
    plt.plot(dates, y2, label="actual")
    plt.xlabel('dates')
    # Set the y axis label of the current axis.
    plt.ylabel('gold price')
    # Set a title of the current axes.
    plt.title('Gold Price prediction')
    plt.legend()

    # Save it to a temporary buffer.
    buf = BytesIO()
    plt.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('index.html', data=data)


app.run(host='0.0.0.0', port=5000)
