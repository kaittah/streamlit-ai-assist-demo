from streamlit_ai_assist import streamlit_ai_assist


DATABASE_NAME = "tastybytes_snowflake"

streamlit_ai_assist(
    graphing_file_path=f"graphing/{DATABASE_NAME}.py",
    graphing_import_path=f"graphing.{DATABASE_NAME}",
    database_name=DATABASE_NAME,
    general_description="This is a food truck menu",
    key="foo_1"
)