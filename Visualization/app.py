import pandas as pd
from flask import Flask, json, request, Response, render_template
import requests
import os
# from resources import visualize
import base64
from io import BytesIO
from matplotlib.figure import Figure

app = Flask(__name__, static_folder="templates")
app.config["DEBUG"] = True


# @app.route("/")
# def visualize():
#     # https://matplotlib.org/3.3.2/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server
#     # Load necessary data
#     preproccesed_data = os.environ["TRAIN_DB_API"]
#     r = requests.get(preproccesed_data)
#     j = r.json()
#     df_preproccesed_data = pd.DataFrame.from_dict(j)
#
#     predicted_data = os.environ["PREDI§CT_DB_API"]
#
#     # Convert to important data
#     original_values = None
#     predicted_values = None
#
#     # Plot model
#     plot_model(original_values, predicted_values)


@app.route('/')
def index():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('index.html', data=data)


app.run(host='0.0.0.0', port=5000)
