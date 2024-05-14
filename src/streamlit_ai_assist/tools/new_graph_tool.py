from src.streamlit_ai_assist.tools.base import ToolInterface
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection
from src.streamlit_ai_assist.agents.function_rewrite_agent import FunctionRewriteAgent
from src.streamlit_ai_assist.agents.llm import ChatLLM

import re

import plotly.express as px
import plotly.graph_objects as go

def format_function(messy_string):
    clean_str = FunctionRewriteAgent(llm=ChatLLM()).rewrite_function(messy_string)
    function_name = re.search(r'def\s+(\w+\(conn\))', clean_str, re.DOTALL)
    if function_name:
        function_name = function_name.group(1)
    return [clean_str, function_name]


class NewGraphTool(ToolInterface):
    
    db: DatabaseConnection
    name: str = "new_graph_tool"

    def get_description(self, docs) -> str:
        description= """Executes the input Python code, returning `fig`, a figure with
relevant information. The input to this action MUST be Python code and MUST follow the following specifications:
###
The code is a Python function with the following requirements.
inputs: `conn`: a database connection. In the body of the code, data is retrieved as a pandas dataframe using pd.read_sql(<sql>, conn) for some
sql statement.
return: `fig`: an instance of plotly.graph_objs.Figure. The function MUST end with `return fig`.
###
"""
        return description
    
    def test_code(self, input_text: str):
        try:
            conn = self.db.connect()
            cleaned_code, function_call = format_function(input_text)
            exec(cleaned_code)
            fig = eval(function_call)
            return 'OK'
        except Exception as e:
            return str(e)

    def use(self, input_text: str):
        status = self.test_code(input_text)
        if status == "OK":
            return f"Returned the new figure"
        else:
            return f"An error was encountered in Python: {status}"
