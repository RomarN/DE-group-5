from flask import Flask, json, request, Response
from resources.Database_utilities import create_tb, drop_tb, add_data_records, read_data_records

app = Flask(__name__)


@app.route('/training-db/<table_name>', methods=['POST'])
def create_table(table_name):
    req_data = request.get_json()
    columns = req_data['columns']
    create_tb(table_name, columns)
    return json.dumps({'message': 'a table was created'}, sort_keys=False, indent=4), 200


@app.route('/training-db/<table_name>', methods=['DELETE'])
def delete_table(table_name):
    drop_tb(table_name)
    return json.dumps({'message': 'a table was dropped'}, sort_keys=False, indent=4), 200


@app.route('/training-db/<table_name>', methods=['PUT'])
def update_data(table_name):
    content = request.get_json()
    add_data_records(table_name, content)
    return json.dumps({'message': 'training data were updated'}, sort_keys=False, indent=4), 200


@app.route('/training-db/<table_name>', methods=['GET'])
def read_data(table_name):
    df = read_data_records(table_name)
    df = df.drop(columns=['id'])
    resp = Response(df.to_json(orient='records'), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Max-Age'] = '1000'
    return resp


app.run(host= '0.0.0.0', port=5000)