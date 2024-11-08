import json
from typing import Any, Dict, List
from tools_description import *

TASK_PROMPT = """
You are a system designed to detect a function that correlates to the prompt of the user. 
""".strip()

TOOL_PROMPT = """
# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{tool_text}
</tools>
""".strip()

FORMAT_PROMPT = """
For each function call, return a json object with function name and arguments like that:
{"name": <function-name>, "arguments": <args-json-object>}
""".strip()


def convert_tools(tools: List[Dict[str, Any]]):
    return "\n".join([json.dumps(tool) for tool in tools])

def format_prompt(tools: List[Dict[str, Any]]):
    tool_text = convert_tools(tools)

    return (
        TASK_PROMPT
        + "\n\n"
        + TOOL_PROMPT.format(tool_text=tool_text)
        + "\n\n"
        + FORMAT_PROMPT
        + "\n"
    )