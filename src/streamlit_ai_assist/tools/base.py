from pydantic import BaseModel

class ToolInterface(BaseModel):
    name: str

    def get_description(self, docs: list[str]) -> str:
        raise NotImplementedError("get_description() method not implemented")  # Implement in subclass
    
    def use(self, input_text: str) -> str:
        raise NotImplementedError("use() method not implemented")  # Implement in subclass