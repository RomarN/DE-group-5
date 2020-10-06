import pandas as pd
from flask import Flask, json, request, Response
import requests
import os
from resources import visualize

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def visualize():
    # https://matplotlib.org/3.3.2/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server
    # Load necessary data
    preproccesed_data = os.environ["TRAIN_DB_API"]
    r = requests.get(preproccesed_data)
    j = r.json()
    df_preproccesed_data = pd.DataFrame.from_dict(j)

    predicted_data = os.environ["PREDICT_DB_API"]

    # Convert to important data
    original_values = None
    predicted_values = None

    # Plot model
    plot_model(original_values, predicted_values)



app.run(host='0.0.0.0', port=5000)
