import sqlite3
import re
import os

import pandas as pd

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from streamlit_ai_assist import streamlit_ai_assist

streamlit_ai_assist(
    graphing_file_path="graphing_tastybytes.py",
    graphing_import_path="graphing_tastybytes",
    database_name="tastybytes_snowflake",
    general_description="This is a food truck menu",
    key="foo"
)