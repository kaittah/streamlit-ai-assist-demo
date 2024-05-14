import os
from src.streamlit_ai_assist.tools.base import ToolInterface
import sqlite3
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection

def get_schema(table_name, db):
    sql_driver = db.get_dialect()
    if sql_driver == 'snowflake':
        query = f'DESC table {table_name}'
    else:
        query = f'PRAGMA table_info({table_name})'
    try:
        schema_df = db.query(query)
    except:
        return ''
    schema = f'TABLE {table_name}:\n'
    for index, row in schema_df.iterrow():
        schema = schema + f'{row[0]} {row[1]}'
    return schema


class SchemaTool(ToolInterface):

    db: DatabaseConnection
    name: str= "schema_tool"
    docs: list[str] = []

    def get_description(self) -> str:
        return """Given a comma separated list of database table names, returns the schema of those tables.The input
must be one of the formats: <table_name> OR <table_name_1>,<table_name_2>,...,<table_name_n>"""

    def use(self, input_text: str):
        table_names = input_text.split(',')
        result = ''
        for table_name in table_names:
            result = result + get_schema(table_name, self.db)
        return dict(observation=result, tool=self.name)

