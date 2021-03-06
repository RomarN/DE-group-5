#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import absolute_import

import argparse
import csv
import io
import logging
import pickle
import warnings

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from google.cloud import storage

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
pd.options.mode.chained_assignment = None
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def train_save_model(readable_file, project_id, bucket_name):
    # Open a channel to read the file from GCS
    gcs_file = beam.io.filesystems.FileSystems.open(readable_file)

    # Read it as csv, you can also use csv.reader
    logging.info(gcs_file)
    csv_dict = csv.DictReader(io.TextIOWrapper(gcs_file))
    # json_dict = json.load(gcs_file)

    # Create the DataFrame
    df = pd.DataFrame.from_dict(csv_dict)
    df = df.apply(pd.to_numeric)
    logging.info(df)
    # split into input (X) and output (Y) variables
    x = df.iloc[:, [0, 1, 2]]
    y = df.iloc[:, [3]]
    logging.info(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.05, random_state=1)
    # define model
    kn_clf = KNeighborsClassifier(n_neighbors=6)
    kn_clf.fit(x_train, y_train)
    kn_pred = kn_clf.predict(x_test)
    kn_acc = accuracy_score(y_test, kn_pred)

    # evaluate the model
    text_out = {
        "accuracy": str(kn_acc * 100)
    }

    pickle.dump(kn_clf, open('model.sav', 'wb'))
    # Save to GCS
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('models/model.sav')
    blob.upload_from_filename('model.sav')
    logging.info("Saved the model to GCP bucket")
    return str(text_out)


def run(argv=None, save_main_session=True):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='gs://dataflow-samples/data/kinglear.txt',
        help='Input file to process.')
    parser.add_argument(
        '--output',
        dest='output',
        # CHANGE 1/6: The Google Cloud Storage path is required
        # for outputting the results.
        default='gs://YOUR_OUTPUT_BUCKET/AND_OUTPUT_PREFIX',
        help='Output file to write results to.')

    parser.add_argument(
        '--pid',
        dest='pid',
        help='project id')

    parser.add_argument(
        '--mbucket',
        dest='mbucket',
        help='model bucket name')
    known_args, pipeline_args = parser.parse_known_args(argv)
    print(known_args)
    print(pipeline_args)
    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    # The pipeline will be run on exiting the with block.
    with beam.Pipeline(options=pipeline_options) as p:
        output = (p | 'Create FileName Object' >> beam.Create([known_args.input])
                  | 'TrainAndSaveModel' >> beam.Map(train_save_model, known_args.pid, known_args.mbucket)
                  )
        output | 'Write' >> WriteToText(known_args.output)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()