import datetime
import re
from typing import List, Dict, Tuple

from pydantic import BaseModel

from src.streamlit_ai_assist.agents.llm import ChatLLM
from src.streamlit_ai_assist.agents import prompts


PROMPT_TEMPLATE = prompts.FUNCTION_REWRITE_PROMPT


class FunctionRewriteAgent(BaseModel):
    llm: ChatLLM
    prompt_template: str= PROMPT_TEMPLATE

    def rewrite_function(self, code_str: str):
        generated = self.llm.generate(prompt=code_str, prompt_template=self.prompt_template)
        if len(generated) < 10:
            return self.clean_function(code_str)
        return generated

    def clean_function(self, code_str: str):
        code_str = code_str.replace('```', '').replace('python\n', '')
        return code_str + '\n    return fig'