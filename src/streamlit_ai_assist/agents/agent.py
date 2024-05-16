import datetime
import re
from typing import List, Dict, Tuple

from pydantic import BaseModel

from src.streamlit_ai_assist.agents.llm import ChatLLM
from src.streamlit_ai_assist.agents import prompts
from src.streamlit_ai_assist.tools.base import ToolInterface
from src.streamlit_ai_assist.data.database_connection import DatabaseConnection


FINAL_ANSWER_TOKEN = "Final Answer:"
OBSERVATION_TOKEN = "Observation:"
THOUGHT_TOKEN = "Thought:"
PROMPT_TEMPLATE = prompts.DATA_ANALYST_PROMPT


class Agent(BaseModel):
    llm: ChatLLM
    tools: List[ToolInterface]
    db: DatabaseConnection
    prompt_template: str= PROMPT_TEMPLATE
    max_loops: int = 2
    stop_pattern: List[str] = [f'\n{OBSERVATION_TOKEN}', f'\n\t{OBSERVATION_TOKEN}', '<|im_end|>']

    class Config:
        arbitrary_types_allowed=True

    @property
    def tool_description(self) -> str:
        return "\n".join([f"{tool.name}: {tool.get_description(self.db)}" for tool in self.tools])

    @property
    def tool_names(self) -> str:
        return ",".join([tool.name for tool in self.tools])

    @property
    def tool_by_names(self) -> Dict[str, ToolInterface]:
        return {tool.name: tool for tool in self.tools}

    def run(self, question: str):
        previous_responses = []
        num_loops = 0
        prompt_template = self.prompt_template.format(
                today = datetime.date.today(),
                tool_description=self.tool_description,
                tool_names=self.tool_names,
        )
        prompt_template = prompt_template.replace('#prompt#', '{prompt}')
        output = {'rendered_prompts': [], 'thoughts': [], 'loop_number': [], 'observations': [],
                  'tool': [], 'eval': [], 'exec': [], 'print': []}

        while num_loops < self.max_loops:
            num_loops += 1
            curr_prompt = prompt_template

            for pr in previous_responses:
                curr_prompt = curr_prompt + '<|im_start|>assistant\n' + pr + '<|im_end|>'
            curr_prompt = curr_prompt + f'<|im_start|>assistant\n{THOUGHT_TOKEN}'
            generated, tool, tool_input = self.decide_next_action(prompt=question,
                                                                  prompt_template=curr_prompt)
            
            if not generated:
                previous_responses[-1] = "I need to think again about what to do"
                curr_prompt = prompt_template
                for pr in previous_responses:
                    curr_prompt = curr_prompt + '<|im_start|>assistant\n' + pr + '<|im_end|>'

                generated, tool, tool_input = self.decide_next_action(prompt=question,
                    prompt_template=curr_prompt)
                if not generated:
                    return tool_input, output

            output['rendered_prompts'].append(curr_prompt)
            output['loop_number'].append(num_loops)
            output['thoughts'].append(generated)
            output['tool'].append(tool)


            if tool == 'Final Answer':
                output['observations'].append('Final')
                output["eval"].append(None)
                output["exec"].append(None)
                output["print"].append(None)
                return tool_input, output
            if tool not in self.tool_by_names:
                output['observations'].append('Failed to proceed.')
                output["eval"].append(None)
                output["exec"].append(None)
                output["print"].append(None)
                continue
            
            tool_result = self.tool_by_names[tool].use(tool_input, self.db)
            tool_result_observation = tool_result["observation"]
            output['observations'].append(tool_result_observation)
            output["eval"].append(tool_result.get("eval"))
            output["exec"].append(tool_result.get("exec"))
            output["print"].append(tool_result.get("print"))

            generated += f"\n{OBSERVATION_TOKEN} {tool_result_observation}"
            previous_responses.append(generated)
        return tool_input, output

    def decide_next_action(self, prompt: str, prompt_template: str) -> str:
        generated = self.llm.generate(prompt, prompt_template, stop=self.stop_pattern)
        tool, tool_input = self._parse(generated)
        try_num = 0
        while not tool and try_num < 3:
            generated = self.llm.generate(prompt, prompt_template, stop=self.stop_pattern)
            tool, tool_input = self._parse(generated)
            try_num += 1
        if not tool:
            return None, None, None
        return generated, tool, tool_input

    def _parse(self, generated: str) -> Tuple[str, str]:
        if FINAL_ANSWER_TOKEN in generated:
            return "Final Answer", generated.split(FINAL_ANSWER_TOKEN)[-1].strip()
        regex = r"Action: [\[]?(.*?)[\]]?[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, generated, re.DOTALL)
        if not match:
            return None, None
        tool = match.group(1).strip()
        tool_input = match.group(2)
        return tool, tool_input.strip(" ").strip('"')