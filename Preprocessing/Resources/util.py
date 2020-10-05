import pandas as pd
import numpy as np

import sqlalchemy as db
from sqlalchemy import Column, Float, Table, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine('sqlite:///traindbpreprocessed.db', echo=True)
Base = declarative_base()
Base.metadata.reflect(engine)


def preprocess(df, table_name):
    # Convert the categorical data into binary values
    df_bin = df.join(pd.get_dummies(df.pop('day')))
    df_bin = df_bin.join(pd.get_dummies(df_bin.pop('month')))
    df_bin.pop('sun')
    df_bin.pop('dec')
    area = df.pop('area')
    area = np.log(area + 1)
    df_bin['area'] = area

    column_names = df_bin.columns
    print(column_names)
    create_table(column_names, table_name)
    add_data_records(table_name, df_bin)


def create_table(column_names, table_name):
    conn = engine.connect()
    trans = conn.begin()
    columns = (Column(name, Float, quote=False) for name in column_names)
    v_table = Table(table_name, Base.metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                    extend_existing=True, *columns)
    v_table.create(engine, checkfirst=True)
    trans.commit()


def add_data_records(table_name, df):
    # records = df.to_json(orient='records')
    # records = records.get_json()
    records = df.to_dict(orient='records')
    print("komt ie hier")
    v_table = Base.metadata.tables[table_name]
    query = db.insert(v_table)
    connection = engine.connect()
    trans = connection.begin()
    # connection.execute(query, {"X":8,"Y":6,"FFMC":91.2,"DMC":147.8,"DC":377.2,"ISI":12.7,"temp":19.6,"RH":43,"wind":4.9,"rain":0.0,"area":0.0,"fri":0,"mon":0,"sat":0,"thu":0,"tue":0,"wed":1,"apr":0,"aug":0,"feb":0,"jan":0,"jul":0,"jun":1,"mar":0,"may":0,"nov":0,"oct":0,"sep":0},{"X":8,"Y":6,"FFMC":91.2,"DMC":147.8,"DC":377.2,"ISI":12.7,"temp":19.6,"RH":43,"wind":4.9,"rain":0.0,"area":0.0,"fri":0,"mon":0,"sat":0,"thu":0,"tue":0,"wed":1,"apr":0,"aug":0,"feb":0,"jan":0,"jul":0,"jun":1,"mar":0,"may":0,"nov":0,"oct":0,"sep":0})
    connection.execute(query, records)
    trans.commit()
    print("komt ie hier 2")


def read_data_records(table_name):
    v_table = Base.metadata.tables[table_name]
    connection = engine.connect()
    trans = connection.begin()
    query = db.select([v_table])
    df = pd.read_sql_query(query, con=connection)
    trans.commit()
    return df
