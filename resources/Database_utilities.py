import pandas as pd
import sqlalchemy as db
from sqlalchemy import Column, Float, Table, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine('sqlite:///traindb.db', echo=True)
Base = declarative_base()
Base.metadata.reflect(engine)


def create_tb(table_name, column_names):
    conn = engine.connect()
    trans = conn.begin()
    columns = (
        Column(name, String, quote=False) if name == 'month' or name == 'day' else Column(name, Float, quote=False) for
        name in column_names)
    v_table = Table(table_name, Base.metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                    extend_existing=True, *columns)
    v_table.create(engine, checkfirst=True)
    trans.commit()


def drop_tb(table_name):
    conn = engine.connect()
    trans = conn.begin()
    v_table = Base.metadata.tables[table_name]
    v_table.drop(engine, checkfirst=True)
    trans.commit()


def add_data_records(table_name, records):
    v_table = Base.metadata.tables[table_name]
    query = db.insert(v_table)
    connection = engine.connect()
    trans = connection.begin()
    connection.execute(query, records)
    trans.commit()


def read_data_records(table_name):
    v_table = Base.metadata.tables[table_name]
    connection = engine.connect()
    trans = connection.begin()
    query = db.select([v_table])
    df = pd.read_sql_query(query, con=connection)
    trans.commit()
    return df
