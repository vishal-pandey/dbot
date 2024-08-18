from State import State
from models import model
from prompts.template_query_generater import template_query_generater

schema_description = """{
  "name": {
    "type": "String",
    "description": "Defines the name of the table, in this case, 'tag_usage'."
  },
  "properties": {
    "type": "Object",
    "description": "Contains metadata properties of the table.",
    "keys": {
      "description": {
        "type": "String",
        "description": "A textual description of the table, explaining that it tracks the usage of tags across various entities."
      }
    }
  },
  "refSql": {
    "type": "String",
    "description": "Represents the reference SQL query to retrieve all data from the table."
  },
  "columns": {
    "type": "Array of Objects",
    "description": "A list of columns present in the table, where each object defines a column's attributes.",
    "objectStructure": {
      "name": {
        "type": "String",
        "description": "The name of the column."
      },
      "type": {
        "type": "String",
        "description": "The data type of the column (e.g., 'TINYINT', 'VARCHAR(256)')."
      },
      "notNull": {
        "type": "Boolean",
        "description": "Indicates whether the column must have a value (cannot be null)."
      },
      "expression": {
        "type": "String",
        "description": "An alias or expression for the column, representing how it is referred to in queries."
      },
      "properties": {
        "type": "Object",
        "description": "Contains metadata about the column.",
        "keys": {
          "description": {
            "type": "String",
            "description": "A textual description explaining the purpose of the column."
          }
        }
      }
    }
  },
  "primaryKey": {
    "type": "Array of Strings",
    "description": "A list of column names that together make up the primary key of the table, ensuring each row is uniquely identifiable."
  }
}"""

# GenerateSQLQueryTool - 
def generate_sql_query_tool(state: State):
    """Tool for generating a SQL query.
        Generate a SQL query based on the question and available information."""
    input = {
        "question": state["question"],
        "tables": state["tables"],
        "relevant_tables": state["relevant_tables"],
        "relevant_tables_schemas": state["relevant_tables_schemas"],
        # "relevant_tables_relationships": state["relevant_tables_relationships"],
        # "relevant_tables_sample_data": state["relevant_tables_sample_data"],
        "messages": state["messages"],
        "schema_description": schema_description
    }


    chain = template_query_generater | model
    output = chain.invoke(input)
    sql_query = output.content
    sql_query = sql_query.replace("sql\n", " ")
    sql_query = sql_query.replace("\n", " ")
    sql_query = sql_query.replace("```", " ")
    state["sql_query"] = sql_query
    state["query_error"] = ""
    
    return state