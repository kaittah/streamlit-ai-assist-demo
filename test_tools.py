import sqlite3
import re
import os

import pandas as pd
import graphing, graphing_tastybytes

from src.streamlit_ai_assist.documents import python_to_docs
from src.streamlit_ai_assist.tools import ShowTablesTool, SchemaTool, ShowUniqueTool, SQLTool, GraphTool, NewGraphTool
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


db = DatabaseConnection(name="tastybytes_snowflake")
graphing_file = 'graphing.py'
graphing_lib = graphing_file.replace('.py', '')


schema_tool = SchemaTool()
try:
    st.write(schema_tool.use("menu", db))
except Exception as e:

    st.write("Schema Tool Failed")
    st.error(str(e))


graph_tool = GraphTool(docs=python_to_docs.python_to_docs(graphing_file))
try:
    st.write(graph_tool.use("plot_customer_states", db))
except Exception as e:
    st.write("Graph Tool Failed")
    st.error(str(e))


# new_graph_tool = NewGraphTool(docs=python_to_docs.python_to_docs(graphing_file))
# try:
#     st.write(new_graph_tool.use("""
# def plot_tracks(conn):
#     df_tracks = pd.read_sql(
#         '''SELECT tracks.trackid, genres.name AS genre 
#             FROM tracks 
#             LEFT JOIN genres on tracks.genreid = genres.genreid
#         ''', conn
#     )
#     tracks_per_genre = df_tracks.groupby('genre').size().reset_index(name='Count')
#     fig = px.bar(tracks_per_genre, x='genre', y='Count', title='Number of Tracks per Genre')
#     return fig
# """, db))
# except Exception as e:
#     st.write("New Graph Tool Failed")
#     st.error(str(e))

show_tables_tool = ShowTablesTool()
try:
    st.write(show_tables_tool.use("menu", db))
except Exception as e:
    st.write("Show Tables Tool Failed")
    st.error(str(e))

show_unique_tool = ShowUniqueTool()
try:
    st.write(show_unique_tool.use("(menu, menu_type)", db))
except Exception as e:
    st.write("Show Unique Failed")
    st.error(str(e))

sql_tool = SQLTool()
try:
    st.write(sql_tool.use("Select 1 GROUP BY 1", db))
except Exception as e:
    st.write("SQL Tool Failed")
    st.error(str(e))