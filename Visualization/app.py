import pandas as pd
from flask import Flask, json, request, Response, render_template
import requests
import os
import json
import base64
from io import BytesIO
from matplotlib.figure import Figure

app = Flask(__name__, static_folder="templates")
app.config["DEBUG"] = True


@app.route('/visualize')
def index():

    # Load necessary data
    with open('predict_area') as json_file:
        areas = json.load(json_file)

    original_area = [area['area'] for area in areas]

    db_api = os.environ['PREDICT_DB_API']
    r = requests.get(db_api)
    j = r.json()
    print(j)
    print(j['1'])
    predicted_areas = pd.DataFrame.from_dict(j)

    # Generate the figure **without using pyplot**.
    fig = Figure()
    plt = fig.subplots()
    plt.plot(original_area, label="Original values")
    # plt.plot([1.2, 1.9], label="True values")
    plt.plot(predicted_areas, label="Prediction")

    plt.set_title("Model predictions vs True values")
    plt.set(xlabel = "Predictions", ylabel = "Area in $ha$")
    plt.legend()

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('index.html', data=data)


app.run(host='0.0.0.0', port=5000)
