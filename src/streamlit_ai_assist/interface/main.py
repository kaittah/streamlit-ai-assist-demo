import importlib
import streamlit as st

from src.streamlit_ai_assist.agents.data_analyst_agent import DataAnalystAgent
from src.streamlit_ai_assist.agents.conversational_agent import ConversationalAgent
from src.streamlit_ai_assist.agents.llm import ChatLLM
from src.streamlit_ai_assist.tools import (
    ShowTablesTool,
    SchemaTool,
    ShowUniqueTool,
    SQLTool,
    GraphTool,
    NewGraphTool
)
from src.streamlit_ai_assist.documents import python_to_docs
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


@st.cache_resource
def get_database(database_name):
    return DatabaseConnection(name=database_name)


@st.cache_resource
def load_agents(database_name, general_description, docs):
    db = get_database(database_name)
    data_analyst = DataAnalystAgent(
                llm=ChatLLM(),
                tools=[
                    ShowTablesTool(),
                    SchemaTool(),
                    ShowUniqueTool(),
                    SQLTool(),
                    GraphTool(docs=docs),
                    NewGraphTool()
                ],
                db=db
            )
    conversational_agent = ConversationalAgent(
            llm=ChatLLM(),
            general_description=general_description,
            data_analyst=data_analyst
        )
    return data_analyst, conversational_agent


class DataAnalystChat:

    def __init__(
            self,
            graphing_file_path,
            graphing_import_path,
            database_name,
            general_description
    ):
        self.graphing_file_path: str = graphing_file_path
        self.graphing_import_path: str = graphing_import_path
        self.database_name: str = database_name
        self.general_description: str = general_description

    def run(self):
        docs = python_to_docs.python_to_docs(self.graphing_file_path)
        data_analyst, conversational_agent = load_agents(
            self.database_name,
            self.general_description,
            docs
        )
        db = get_database(self.database_name)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.text(message["content"])

        if prompt := st.chat_input("Ask me a question about your data"):
            conversational_agent.clear_data()
            with st.chat_message("user"):
                st.text(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

            next_message, results_list = conversational_agent.run(prompt)

            for row in results_list:

                if row["eval"] and row["tool"] == "graph_tool":
                    conn = db.connect()
                    imported_graphing_library = importlib.import_module(self.graphing_import_path)
                    func = eval(f'imported_graphing_library.{row["eval"]}')
                    fig = func(conn)

                    with st.chat_message("assistant"):
                        st.plotly_chart(fig, use_container_width=True)

                elif row["eval"] and row["exec"] and row["tool"] == "new_graph_tool":
                    conn = db.connect()
                    exec(row["exec"])
                    fig = eval(row["eval"])
                    with st.chat_message("assistant"):
                        st.plotly_chart(fig, use_container_width=True)

                elif row["print"]:
                    if isinstance(row["dataframe"], pd.DataFrame):
                        with st.chat_message("assistant"):
                            st.dataframe(row["dataframe"])
                    else:
                        with st.chat_message("assistant"):
                            st.text(row["print"])

            with st.chat_message("assistant"):
                st.text(next_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": next_message}
                )
