from flask import Flask, json, request, Response, render_template
import requests
import os
import json
import base64
from io import BytesIO
# from matplotlib.figure import Figure

import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix

app = Flask(__name__, static_folder="templates")
app.config["DEBUG"] = True


@app.route('/visualize')
def index():


    # Load necessary data
    results = pd.read_csv('results_predictions-00000-of-00001.csv', header=None, names=['predicted', 'actual'])


    # Generate the figure **without using pyplot**.


    cm = confusion_matrix(results['actual'], results['predicted'])
    plt.figure()
    plot_confusion_matrix(cm, figsize=(12, 8), hide_ticks=True, cmap=plt.cm.Blues)
    plt.title("K Neighbors Model - Confusion Matrix")
    plt.xticks(range(2), ["Heart Not Failed", "Heart Fail"], fontsize=16)
    plt.yticks(range(2), ["Heart Not Failed", "Heart Fail"], fontsize=16)
    # Save it to a temporary buffer.
    buf = BytesIO()
    plt.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('index.html', data=data)


app.run(host='0.0.0.0', port=5000)
