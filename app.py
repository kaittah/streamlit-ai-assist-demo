import sqlite3

import graphing

from src.streamlit_ai_assist.documents import python_to_docs, docs_to_function_names
from src.streamlit_ai_assist.retrieval import retrieve_top_k

import streamlit as st

db_file = 'chinook/chinook.db'
graphing_file = 'graphing.py'
graphing_library = 'graphing'

query= st.text_input("Ask a question about the data")
if not query:
    query = "Show me tracks by genre"
docs = python_to_docs.python_to_docs(graphing_file)
top_k_docs = retrieve_top_k.retrieve_top_k(query=query, docs=docs, k=5)
function_names = docs_to_function_names.extract_function_names(top_k_docs)
functions = [eval(f'{graphing_library}.{name}') for name in function_names if name in dir(eval(graphing_library))]

with sqlite3.connect(db_file) as conn:
    figs = [func(conn) for func in functions]

for fig in figs:
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)

