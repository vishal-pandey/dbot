from State import State
from databases import db

# InfoSQLDatabaseTool
def info_sql_database_tool(state: State):
    """Tool for getting metadata about a SQL database.
        A comma-separated list of the table names for which to return the schema.
        Example input: 'table1, table2, table3'
        Get the schema and sample rows for the specified SQL tables."""
    
    tableinfo = db.get_table_info_no_throw(
            [t.strip() for t in state["relevant_tables"].split(",")]
        )
    
    state["query_error"] = ""
    state["retry_count"] = 0
    state["relevant_tables_sample_data"] = str(tableinfo)
    return state
