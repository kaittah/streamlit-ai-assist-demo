from src.streamlit_ai_assist.tools.base import ToolInterface
import pandas as pd
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection

def dataframe_to_text_table(df: pd.DataFrame) -> str:
    table_str = df.to_string(index=False)
    rows = table_str.split('\n')
    headers = rows[0]
    header_line = '-'*len(headers)
    formatted_table = [headers, header_line] + rows[1:]
    formatted_table_str = '\n'.join(formatted_table)
    return formatted_table_str
        
def query_to_text_table(query, db):
    if 'group by' not in query.lower():
        return "ERROR", "Error: The SQL query does not include a group by clause. Too many rows would be returned."
    try:
        df = db.query(query)
        n_rows = df.shape[0]
        n_cols = df.shape[1]
        if n_rows < 20 and n_cols < 4:
            return "OK", dataframe_to_text_table(df)
        else:
            return "ERROR", f"""The resulting table is too large.
The dimensions are {n_rows} rows by {n_cols} cols. There can be at most 20 rows and 4 columns. This tool
can only be used to summarize data. Choose another action. """
    except Exception as e:
        return "ERROR", f'The SQL query failed with error: {str(e)}. Choose another Action.'

class SQLTool(ToolInterface):
    name: str= "sql_tool"
    docs: list[str] = []
    
    def get_description(self, db) -> str:
        dialect = db.get_dialect()
        return f"""Executes the given sql query against a given database with dialect {dialect} and returns a table of results.
You must ONLY use this with queries with GROUP BY clauses in order to answer a question or describe a graph.
"""

    def use(self, input_text: str, db):
        status, table = query_to_text_table(input_text, db)
        if status == "OK":
            return dict(observation=table, tool=self.name, print=table)
        else:
            return dict(observation=table, tool=self.name)
