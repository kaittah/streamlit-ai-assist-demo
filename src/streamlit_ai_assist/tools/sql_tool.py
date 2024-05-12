import os
from src.streamlit_ai_assist.tools.base import ToolInterface
import sqlite3
import pandas as pd

def dataframe_to_text_table(df: pd.DataFrame) -> str:
    table_str = df.to_string(index=False)
    rows = table_str.split('\n')

    headers = rows[0].split()
    header_line = [('-' * len(header)) for header in headers]
    formatted_table = [headers, header_line] + [row.split() for row in rows[1:]]
    col_widths = [max(len(row[i]) for row in formatted_table) for i in range(len(headers))]
    formatted_rows = [' '.join(f'{value:{width}}' for value, width in zip(row, col_widths)) for row in formatted_table]
    formatted_table_str = '\n'.join(formatted_rows)

    return formatted_table_str
        
def query_to_text_table(query):
    db_file = os.environ.get('db_filename')
    with sqlite3.connect(db_file) as conn:
        try:
            df = pd.read_sql(query, conn)
            return dataframe_to_text_table(df)
        except Exception as e:
            return f'The SQL query failed with error: {str(e)}'

class SQLTool(ToolInterface):
    name: str= "sql_tool"
    
    def get_description(self, docs) -> str:
        return "Executes the given sql query against a given database and returns a table of results"

    def use(self, input_text: str):
        return query_to_text_table(input_text)
