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


db = DatabaseConnection(name="chinook_sqlite")
graphing_file = 'graphing.py'
graphing_lib = graphing_file.replace('.py', '')


schema_tool = SchemaTool(db=db)
try:
    st.write(schema_tool.use("tracks"))
except:
    st.write("Schema Tool Failed")

graph_tool = GraphTool(db=db, docs=python_to_docs.python_to_docs(graphing_file))
try:
    st.write(graph_tool.use("plot_customer_states"))
except:
    st.write("Graph Tool Failed")

new_graph_tool = NewGraphTool(db=db, docs=python_to_docs.python_to_docs(graphing_file))
try:
    st.write(new_graph_tool.use("""
def plot_tracks(conn):
    df_tracks = pd.read_sql(
        '''SELECT tracks.trackid, genres.name AS genre 
            FROM tracks 
            LEFT JOIN genres on tracks.genreid = genres.genreid
        ''', conn
    )
    tracks_per_genre = df_tracks.groupby('genre').size().reset_index(name='Count')
    fig = px.bar(tracks_per_genre, x='genre', y='Count', title='Number of Tracks per Genre')
    return fig
"""))
except:
    st.write("New Graph Tool Failed")

show_tables_tool = ShowTablesTool(db=db)
try:
    st.write(show_tables_tool.use("tracks,invoice_items"))
except:
    st.write("Show Tables Tool Failed")

show_unique_tool = ShowUniqueTool(db=db)
try:
    st.write(show_unique_tool.use("(tracks, genreid)"))
except:
    st.write("Show Unique Failed")

sql_tool = SQLTool(db=db)
try:
    st.write(sql_tool.use("Select 1 GROUP BY 1"))
except:
    st.write("SQL Tool Failed")