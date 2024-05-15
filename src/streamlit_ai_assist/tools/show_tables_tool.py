import streamlit as st

from src.streamlit_ai_assist.tools.base import ToolInterface
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection

def get_tables(db):
    sql_driver = db.get_dialect()
    if sql_driver == 'snowflake':
        st.cache_data.clear()
        query = 'SHOW TERSE TABLES'
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        names = [r[1] for r in results]
    else:
        query = "SELECT name as name FROM sqlite_schema WHERE type ='table' AND  name NOT LIKE 'sqlite_%'"
        df = db.query(query)
        names = df['name'].unique()
    tables = "These tables exist: "
    for name in names:
        tables = tables + f'{name} '
    return tables


class ShowTablesTool(ToolInterface):

    name: str= "show_tables_tool"
    docs: list[str] = []

    def get_description(self) -> str:
        return """Given a max number of tables to display (suggested: 50), shows which tables exist in the database. The input must be an integer, e.g. 50. """

    def use(self, input_text: str, db):
        result = get_tables(db)
        return dict(observation=result, tool=self.name)

