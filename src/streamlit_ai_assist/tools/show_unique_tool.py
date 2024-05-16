from src.streamlit_ai_assist.tools.base import ToolInterface
import pandas as pd
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection
import re

def dataframe_to_text_table(df: pd.DataFrame) -> str:
    table_str = df.to_string(index=False)
    rows = table_str.split('\n')
    headers = rows[0]
    header_line = '-'*len(headers)
    formatted_table = [headers, header_line] + rows[1:]
    formatted_table_str = '\n'.join(formatted_table)
    return formatted_table_str
        
def query_to_text_table(query, db):
    try:
        df = db.query(query)
        return "OK", dataframe_to_text_table(df)
    except Exception as e:
        return "ERROR", f'Failed with error: {str(e)}. Choose another Action.'

class ShowUniqueTool(ToolInterface):

    name: str= "show_unique_tool"
    docs: list[str] = []
    
    def get_description(self, db) -> str:
        return f"""Given a table name and a column, returns which unique values exist in the column of the table.
Useful for showing which values of a categorical value exist so that filters can be created down the line. Input to this tool
MUST use the format (<table name>, <column name>). E.g. (zoo, species)
"""

    def use(self, input_text: str, db):
        match = re.findall(r'\((\w+),\s*(\w+)\)', input_text)[0]
        table_name = match[0]
        column_name = match[1]
        query = f"SELECT DISTINCT {column_name} FROM {table_name} LIMIT 50"
        status, table = query_to_text_table(query, db)
        if status == "OK":
            return dict(observation=table, tool=self.name, print=table)
        else:
            return dict(observation=table, tool=self.name)