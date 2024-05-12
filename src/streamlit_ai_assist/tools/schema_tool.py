import os
from src.streamlit_ai_assist.tools.base import ToolInterface
import sqlite3

def get_schema(table_name):
    db_file = os.environ.get('db_filename')
    with sqlite3.connect(db_file) as conn:
        try:
            cur = conn.cursor()
            cur.execute(f'PRAGMA table_info({table_name})')
            result = cur.fetchall()
            schema = f'TABLE {table_name}:\n'
            for col in result:
                schema = schema + f'{col[1]} {col[2]}'
            return schema
        except:
            return ''
        


class SchemaTool(ToolInterface):
    name: str= "schema_tool"

    def get_description(self, docs) -> str:
        return "Given a comma separated list of database table names, returns the schema of those tables"

    def use(self, input_text: str):
        table_names = input_text.split(',')
        result = ''
        for table_name in table_names:
            result = result + get_schema(table_name)
        return result

