

# QuerySQLCheckerTool
from pyexpat import model
from State import State
from prompts.template_query_checker import template_query_checker


def query_sql_checker_tool(state: State):
    """Tool for checking a SQL query.
        Input is a SQL query string, output is a boolean indicating whether the query is valid.
        Check the syntax of a SQL query and return a boolean indicating whether the query is valid."""
    
    input = {}
    input["query"] = state["sql_query"]
    input["query_error"] = state["query_error"]
    input["relevant_tables_schemas"] = state["relevant_tables_schemas"]

    chain = template_query_checker | model
    output = chain.invoke(input)
    sql_query = output.content
    sql_query = sql_query.replace("sql\n", " ")
    sql_query = sql_query.replace("\n", " ")
    sql_query = sql_query.replace("```", " ")
    state["sql_query"] = sql_query
    state["query_error"] = ""
    return state