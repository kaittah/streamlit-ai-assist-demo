from src.streamlit_ai_assist.tools.base import ToolInterface

class GraphTool(ToolInterface):
    
    name: str = "graph_tool"

    def get_description(self, docs) -> str:
        description= """Given a function name, 
executes the below function with that name and displays the figure to the end customer.
Using the functions below, you can infer names of tables in the database and relationships you
can use to write a SQL query. If using the graph_tool in this step, in the next steps, you must
get a summary of the data in the graph using SQL.
Available functions:

"""
        for s in docs:
            description = description + s
        return description

    def use(self, input_text: str):
        return f"Displayed graph with function name {input_text}"
