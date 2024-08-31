from State import State
from dbragtool import getListOfAllTables, getListOfTables, getRelationshipsForTables

# ListSQLDatabaseTool
# Tool for getting tables names related to application, do not use it if user is asking for the table, for that you should query table_entity.
def list_sql_database_tool(state: State):
    """Tool for getting tables names.
        Input is an empty string, output is a comma-separated list of tables in the database.

        Get the question from the state and return the list of tables in the database.
    """
    state["tables"] = getListOfAllTables()
    op = getListOfTables(state["question"])
    state["relevant_tables"] = ", ".join(op["tables"])
    state["relevant_tables_schemas"] = str(op["schemas"])
    state["relevant_tables_relationships"] = str(getRelationshipsForTables(op["tables"]))
    return state