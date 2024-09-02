from langgraph.graph import StateGraph, START, END
# from nodes import list_sql_database_tool, info_sql_database_tool, generate_sql_query_tool, query_sql_database_tool, query_sql_checker_tool, generate_answer_for_user, decide_query_or_not
from nodes.decide_query_or_not import decide_query_or_not
from nodes.generate_answer_for_user import generate_answer_for_user
from nodes.generate_sql_query_tool import generate_sql_query_tool
from nodes.info_sql_database_tool import info_sql_database_tool
from nodes.list_sql_database_tool import list_sql_database_tool
from nodes.query_sql_checker_tool import query_sql_checker_tool
from nodes.query_sql_database_tool import query_sql_database_tool
from nodes.call_db_model import call_db_model, call_db_info_model, trasfer_temp_to_messages
from nodes.db_tools_node import db_tools_node, db_tools_info_node


from State import State

GraphBuilder = StateGraph(State)

# def route_tool(state: State):
#     if "Error: " in state["query_result"] and state["retry_count"] < 3:
#         return "query_sql_checker_tool"
#     else:
#         return "generate_answer_for_user"
    
# def route_query(state: State):
#     if state["is_query"] == "yes":
#         return "list_sql_database_tool"
#     else:
#         return "__end__"



def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "db_tools_node"
    return "__end__"


def route_tools_query(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("temp_messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "db_tools_info_node"
    return "trasfer_temp_to_messages"

GraphBuilder.add_node("list_sql_database_tool", list_sql_database_tool)
GraphBuilder.add_node("info_sql_database_tool", info_sql_database_tool)
GraphBuilder.add_node("generate_sql_query_tool", generate_sql_query_tool)
GraphBuilder.add_node("query_sql_database_tool", query_sql_database_tool)
GraphBuilder.add_node("generate_answer_for_user", generate_answer_for_user)
GraphBuilder.add_node("query_sql_checker_tool", query_sql_checker_tool)
GraphBuilder.add_node("decide_query_or_not", decide_query_or_not)
GraphBuilder.add_node("call_db_model", call_db_model)
GraphBuilder.add_node("call_db_info_model", call_db_info_model)
GraphBuilder.add_node("db_tools_node", db_tools_node)
GraphBuilder.add_node("db_tools_info_node", db_tools_info_node)
GraphBuilder.add_node("trasfer_temp_to_messages", trasfer_temp_to_messages)




# GraphBuilder.add_edge(START, "decide_query_or_not")

# GraphBuilder.add_conditional_edges(
#     "decide_query_or_not",
#     route_query
# )

GraphBuilder.add_edge(START, "list_sql_database_tool")
GraphBuilder.add_edge("list_sql_database_tool", "info_sql_database_tool")
GraphBuilder.add_edge("list_sql_database_tool", "call_db_model")

GraphBuilder.add_edge("db_tools_node", "call_db_model")
# GraphBuilder.add_edge("db_tools_info_node", "call_db_info_model")
# GraphBuilder.add_edge("trasfer_temp_to_messages", "call_db_model")

GraphBuilder.add_conditional_edges(
    "call_db_model",
    route_tools
)

# GraphBuilder.add_conditional_edges(
#     "call_db_info_model",
#     route_tools_query
# )

# GraphBuilder.add_edge("info_sql_database_tool", "generate_sql_query_tool")
# GraphBuilder.add_edge("generate_sql_query_tool", "query_sql_database_tool")
# GraphBuilder.add_edge("query_sql_checker_tool", "query_sql_database_tool")

# GraphBuilder.add_conditional_edges(
#     "query_sql_database_tool",
#     route_tool
# )

# GraphBuilder.add_edge("generate_answer_for_user", "__end__")
