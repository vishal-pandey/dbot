from langgraph.graph import StateGraph, START, END
from MetadataToolkitNodes import list_sql_database_tool, info_sql_database_tool, generate_sql_query_tool, query_sql_database_tool, query_sql_checker_tool, generate_answer_for_user
from State import State

GraphBuilder = StateGraph(State)

def route_tool(state: State):
    if "Error: " in state["query_result"] and state["retry_count"] < 3:
        return "query_sql_checker_tool"
    else:
        return "generate_answer_for_user"

GraphBuilder.add_node("list_sql_database_tool", list_sql_database_tool)
GraphBuilder.add_node("info_sql_database_tool", info_sql_database_tool)
GraphBuilder.add_node("generate_sql_query_tool", generate_sql_query_tool)
GraphBuilder.add_node("query_sql_database_tool", query_sql_database_tool)
GraphBuilder.add_node("generate_answer_for_user", generate_answer_for_user)
GraphBuilder.add_node("query_sql_checker_tool", query_sql_checker_tool)


GraphBuilder.add_edge(START, "list_sql_database_tool")
GraphBuilder.add_edge("list_sql_database_tool", "info_sql_database_tool")
GraphBuilder.add_edge("info_sql_database_tool", "generate_sql_query_tool")
GraphBuilder.add_edge("generate_sql_query_tool", "query_sql_database_tool")
GraphBuilder.add_edge("query_sql_checker_tool", "query_sql_database_tool")

GraphBuilder.add_conditional_edges(
    "query_sql_database_tool",
    route_tool
)

GraphBuilder.add_edge("generate_answer_for_user", "__end__")
