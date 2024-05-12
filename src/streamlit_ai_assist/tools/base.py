from pydantic import BaseModel
from streamlit.connections import SQLConnection

class ToolInterface(BaseModel):
    
    db: SQLConnection
    name: str

    class Config:
        arbitrary_types_allowed = True

    def get_description(self, docs: list[str]) -> str:
        raise NotImplementedError("get_description() method not implemented")  # Implement in subclass
    
    def use(self, input_text: str) -> str:
        raise NotImplementedError("use() method not implemented")  # Implement in subclass