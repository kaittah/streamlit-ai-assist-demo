import sqlite3
import re

import pandas as pd
import graphing

from src.streamlit_ai_assist.documents import python_to_docs, docs_to_function_names
from src.streamlit_ai_assist.retrieval import retrieve_top_k
from src.streamlit_ai_assist.agents.agent import Agent
from src.streamlit_ai_assist.agents.llm import ChatLLM
from src.streamlit_ai_assist.tools import SchemaTool, SQLTool, GraphTool

import streamlit as st

db_file = 'chinook/chinook.db'
graphing_file = 'graphing.py'
graphing_library = 'graphing'

query = None
query = st.text_input("Ask a question about the data")
if not query:
    query = "what are the top 3 most popular genres according to number of tracks?"
docs = python_to_docs.python_to_docs(graphing_file)
top_k_docs = retrieve_top_k.retrieve_top_k(query=query, docs=docs, k=5)
top_k_function_names = docs_to_function_names.extract_function_names(top_k_docs)
function_names = []

agent = Agent(llm=ChatLLM(), tools=[SchemaTool(), SQLTool(), GraphTool()], docs=docs)
result, agent_outputs = agent.run(query)

pattern = r'\.\nAction: graph_tool\nAction Input: (\w+)\(.*?\)'

agent_outputs_df = pd.DataFrame(agent_outputs)
st.write(agent_outputs_df)

for pr in agent_outputs_df['thoughts'].unique():
    st.write(pr)
    match = re.search(pattern, pr)
    if match:
        function_name = match.group(1)
        function_names.append(function_name)

functions = [eval(f'{graphing_library}.{name}') for name in function_names if name in dir(eval(graphing_library))]

with sqlite3.connect(db_file) as conn:
    figs = [func(conn) for func in functions]

for fig in figs:
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)


st.write(result)