import sqlite3
import re
import os

import pandas as pd
import graphing, graphing_tastybytes

from src.streamlit_ai_assist.documents import python_to_docs, docs_to_function_names
from src.streamlit_ai_assist.retrieval import retrieve_top_k
from src.streamlit_ai_assist.agents.agent import Agent
from src.streamlit_ai_assist.agents.function_rewrite_agent import FunctionRewriteAgent
from src.streamlit_ai_assist.agents.llm import ChatLLM
from src.streamlit_ai_assist.tools import ShowTablesTool, SchemaTool, ShowUniqueTool, SQLTool, GraphTool, NewGraphTool
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


graphing_file = 'graphing.py'
graphing_lib = graphing_file.replace('.py', '')


query = st.text_input("Ask a question about the data")
# if not query:
#     query = "can you show me a graph showing ranked menu items by price? I only care about the 'menu type' that includes hot dogs. I'm not sure if the menu type is named hot dogs or a similar wording"
db = DatabaseConnection(name='tastybytes_snowflake')
db = DatabaseConnection(name="chinook_sqlite")

if query:
    docs = python_to_docs.python_to_docs(graphing_file)
    top_k_docs = retrieve_top_k.retrieve_top_k(query=query, docs=docs, k=5)
    top_k_function_names = docs_to_function_names.extract_function_names(top_k_docs)

    agent = Agent(llm=ChatLLM(), tools=[ShowTablesTool(db=db), SchemaTool(db=db), ShowUniqueTool(db=db), SQLTool(db=db), GraphTool(db=db, docs=docs), NewGraphTool(db=db)])
    result, agent_outputs = agent.run(query)

    agent_outputs_df = pd.DataFrame(agent_outputs)

    st.write(agent_outputs_df)

    for index, row in agent_outputs_df.iterrows():
        if row["eval"] and row["tool"] == "graph_tool":
            conn = db.connect()
            func = eval(f'{graphing_lib}.{row["eval"]}')
            fig = func(conn)
            with st.container(border=True):
                st.plotly_chart(fig, use_container_width=True)
        elif row["eval"] and row["exec"] and row["tool"] == "new_graph_tool":
            conn = db.connect()
            exec(row["exec"])
            fig = eval(row["eval"])
            with st.container(border=True):
                st.plotly_chart(fig, use_container_width=True)

    st.write(result)