from streamlit.connections import SnowflakeConnection
import streamlit as st

class DatabaseConnection():
    
    def __init__(self, name: str):
        self.name = name
        self.conn = st.connection(self.name)

    def get_dialect(self):
        if isinstance(self.conn, SnowflakeConnection):
            return "snowflake"
        else:
            return self.conn.engine.dialect.name
        
    def query(self, sql):
        return self.conn.query(sql)
    
    def connect(self):
        return self.conn.engine.raw_connection()