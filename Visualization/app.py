import pandas as pd
from flask import Flask, json, request, Response, render_template
import requests
import os
import base64
from io import BytesIO
from matplotlib.figure import Figure

app = Flask(__name__, static_folder="templates")
app.config["DEBUG"] = True


@app.route('/visualize')
def index():
    # Load necessary data
    # preproccesed_data = os.environ["PREPROCESS_DB_API"]
    # r = requests.get(preproccesed_data)
    # j = r.json()
    # df_preproccesed_data = pd.DataFrame.from_dict(j)

    # Convert to important data
    # original_values = df_preproccesed_data.pop("area")
    predicted_values = None

    # Generate the figure **without using pyplot**.
    fig = Figure()
    plt = fig.subplots()
    # plt.plot(original_values, label="True values")
    plt.plot([1.2, 1.9], label="True values")
    plt.plot([1, 2], label="Prediction")

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
