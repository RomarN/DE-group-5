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
import json
import logging
import pickle
import warnings

import apache_beam as beam
from apache_beam.io import WriteToText, ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from google.cloud import storage

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
pd.options.mode.chained_assignment = None
from sklearn.model_selection import train_test_split


# def preprocess_data(readable_file, project_id, bucket_name):
#     # Open a channel to read the file from GCS
#     gcs_file = beam.io.filesystems.FileSystems.open(readable_file)
#
#     # Read it as csv, you can also use csv.reader
#     csv_dict = csv.DictReader(io.TextIOWrapper(gcs_file))
#
#     # Create the DataFrame
#     df = pd.DataFrame(csv_dict)
#
#     # split into input (X) and output (Y) variables
#     x = df.iloc[:, [11, 4, 7]]
#     y = df.iloc[:, [12]]
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)
#     logging.info(x_train)
#     train = pd.concat([x_train, y_train], axis=1)
#     test = pd.concat([x_test, y_test],axis=1)
#     return train, test


def split_dataset(plant, num_partitions, ratio):
    assert num_partitions == len(ratio)
    bucket = sum(map(ord, json.dumps(plant))) % sum(ratio)
    total = 0
    for i, part in enumerate(ratio):
        total += part
        if bucket < total:
            return i
    return len(ratio) - 1

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
        train_dataset, test_dataset = (p | 'Create FileName Object' >> ReadFromText(known_args.input)
                                       | 'Train_Test_Split' >> beam.Partition(split_dataset, 2, ratio=[8, 2]))
        train_dataset | 'Write' >> WriteToText(known_args.output, file_name_suffix=".csv")
        test_dataset | 'Write_test' >> WriteToText(known_args.output + "TEST", file_name_suffix=".csv")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()