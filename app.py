import sqlite3
import re
import os

import pandas as pd
import graphing

from src.streamlit_ai_assist.documents import python_to_docs, docs_to_function_names
from src.streamlit_ai_assist.retrieval import retrieve_top_k
from src.streamlit_ai_assist.agents.agent import Agent
from src.streamlit_ai_assist.agents.llm import ChatLLM
from src.streamlit_ai_assist.tools import SchemaTool, SQLTool, GraphTool
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection

import streamlit as st


graphing_file = 'graphing.py'
graphing_lib = graphing_file.replace('.py', '')


query = st.text_input("Ask a question about the data")
db = DatabaseConnection(name='chinook_sqlite')
if query:
    docs = python_to_docs.python_to_docs(graphing_file)
    top_k_docs = retrieve_top_k.retrieve_top_k(query=query, docs=docs, k=5)
    top_k_function_names = docs_to_function_names.extract_function_names(top_k_docs)
    used_function_names = []


    agent = Agent(llm=ChatLLM(), tools=[SchemaTool(db=db), SQLTool(db=db), GraphTool(db=db)], docs=docs)
    result, agent_outputs = agent.run(query)

    pattern = r'\.\nAction: graph_tool\nAction Input: (\w+)\(.*?\)'

    agent_outputs_df = pd.DataFrame(agent_outputs)

    st.write(agent_outputs_df)

    for previous_response in agent_outputs_df['thoughts'].unique():
        st.write(previous_response)
        match = re.search(pattern, previous_response)
        if match:
            function_name = match.group(1)
            used_function_names.append(function_name)

    functions = [eval(f'{graphing_lib}.{name}') for name in used_function_names if name in dir(eval(graphing_lib))]

    conn = db.connect()
    figs = [func(conn) for func in functions]

    for fig in figs:
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)


    st.write(result)