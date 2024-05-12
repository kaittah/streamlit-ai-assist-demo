from src.streamlit_ai_assist.tools.base import ToolInterface
import pandas as pd
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection

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
        
def query_to_text_table(query, db):
    try:
        df = db.query(query)
        return dataframe_to_text_table(df)
    except Exception as e:
        return f'The SQL query failed with error: {str(e)}. Choose another Action.'

class SQLTool(ToolInterface):
    db: DatabaseConnection
    name: str= "sql_tool"
    
    def get_description(self, docs) -> str:
        dialect = self.db.get_dialect()
        return f"Executes the given sql query against a given database with dialect {dialect} and returns a table of results"

    def use(self, input_text: str):
        return query_to_text_table(input_text, self.db)
