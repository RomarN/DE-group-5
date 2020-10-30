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
    blob = bucket.blob('results/predictions-00000-of-00001.csv')
    blob.download_to_filename('download.csv')
    csv_file = pickle.load(open('download.csv', 'rb'))

    # Load necessary data
    results = pd.read_csv(csv_file, header=None, names=['predicted', 'actual'])

    # Generate the figure **without using pyplot**.
    cm = confusion_matrix(results['actual'], results['predicted'])
    plt.figure()
    plot_confusion_matrix(cm, figsize=(7.5, 5), hide_ticks=True, cmap=plt.cm.Blues)
    plt.title("K Neighbors Model - Confusion Matrix")
    plt.xticks(range(2), ["Heart Not Failed", "Heart Fail"], fontsize=16)
    plt.yticks(range(2), ["Heart Not Failed", "Heart Fail"], fontsize=16, rotation=45)
    # Save it to a temporary buffer.
    buf = BytesIO()
    plt.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('index.html', data=data)


app.run(host='0.0.0.0', port=5000)
