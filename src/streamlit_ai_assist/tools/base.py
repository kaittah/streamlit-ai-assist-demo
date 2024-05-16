from pydantic import BaseModel

class ToolInterface(BaseModel):
    
    name: str
    docs: list[str]

    class Config:
        arbitrary_types_allowed = True

    def get_description(self, db) -> str:
        raise NotImplementedError("get_description() method not implemented")  # Implement in subclass
    
    def use(self, input_text: str, db) -> dict[str]:
        raise NotImplementedError("use() method not implemented")  # Implement in subclass