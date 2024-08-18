from State import State
from databases import db

# QuerySQLDataBaseTool
def query_sql_database_tool(state: State):
    """Tool for querying a SQL database.
        Input is a SQL query string, output is the result of the query.
        Execute a SQL query against the database and get back the result..
        If the query is not correct, an error message will be returned.
        If an error is returned, rewrite the query, check the query, and try again."""
    
    response = db.run_no_throw(state["sql_query"])
    state["query_result"] = str(response)
    
    state["retry_count"] = state["retry_count"] + 1
    if "Error: " in state["query_result"] and state["retry_count"] < 3:
        state["query_error"] = state["query_result"]
    else:
        state["query_error"] = ""
    return state