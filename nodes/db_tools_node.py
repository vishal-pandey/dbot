from toolkits.SQLDatabaseToolkit import SQLDatabaseToolkit
from databases import db
from models import model
from State import State
import json
from langchain_core.messages import ToolMessage

# class BasicToolNode:
#     """A node that runs the tools requested in the last AIMessage."""

#     def __init__(self, state: State) -> None:
#         sqltoolkit = SQLDatabaseToolkit(db=db, llm=model, state=state)
#         tools = sqltoolkit.get_tools()

#         self.tools_by_name = {tool.name: tool for tool in tools}

#     def __call__(self, inputs: dict):
#         if messages := inputs.get("messages", []):
#             message = messages[-1]
#         else:
#             raise ValueError("No message found in input")
#         outputs = []
#         for tool_call in message.tool_calls:
#             tool_result = self.tools_by_name[tool_call["name"]].invoke(
#                 tool_call["args"]
#             )
#             outputs.append(
#                 ToolMessage(
#                     content=json.dumps(tool_result),
#                     name=tool_call["name"],
#                     tool_call_id=tool_call["id"],
#                 )
#             )
#         return {"messages": outputs}
    

def db_tools_node(state: State):
    sqltoolkit = SQLDatabaseToolkit(db=db, llm=model, state=state)
    tools = sqltoolkit.get_tools()
    tools_by_name = {tool.name: tool for tool in tools}

    if messages := state.get("messages", []):
        message = messages[-1]
    else:
        raise ValueError("No message found in input")
    outputs = []
    for tool_call in message.tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(
            tool_call["args"]
        )
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}


def db_tools_info_node(state: State):
    sqltoolkit = SQLDatabaseToolkit(db=db, llm=model, state=state)
    tools = sqltoolkit.get_tools()
    tools_by_name = {tool.name: tool for tool in tools}

    if messages := state.get("temp_messages", []):
        message = messages[-1]
    else:
        raise ValueError("No message found in input")
    outputs = []
    for tool_call in message.tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(
            tool_call["args"]
        )
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"temp_messages": outputs}




# db_tools_node = basic_tool_node(state=State)