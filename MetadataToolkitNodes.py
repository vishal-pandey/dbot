# from State import State
# from dbragtool import getListOfAllTables, getListOfTables, getRelationshipsForTables
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
# from models import model
# from databases import db

# schema_description = """{
#   "name": {
#     "type": "String",
#     "description": "Defines the name of the table, in this case, 'tag_usage'."
#   },
#   "properties": {
#     "type": "Object",
#     "description": "Contains metadata properties of the table.",
#     "keys": {
#       "description": {
#         "type": "String",
#         "description": "A textual description of the table, explaining that it tracks the usage of tags across various entities."
#       }
#     }
#   },
#   "refSql": {
#     "type": "String",
#     "description": "Represents the reference SQL query to retrieve all data from the table."
#   },
#   "columns": {
#     "type": "Array of Objects",
#     "description": "A list of columns present in the table, where each object defines a column's attributes.",
#     "objectStructure": {
#       "name": {
#         "type": "String",
#         "description": "The name of the column."
#       },
#       "type": {
#         "type": "String",
#         "description": "The data type of the column (e.g., 'TINYINT', 'VARCHAR(256)')."
#       },
#       "notNull": {
#         "type": "Boolean",
#         "description": "Indicates whether the column must have a value (cannot be null)."
#       },
#       "expression": {
#         "type": "String",
#         "description": "An alias or expression for the column, representing how it is referred to in queries."
#       },
#       "properties": {
#         "type": "Object",
#         "description": "Contains metadata about the column.",
#         "keys": {
#           "description": {
#             "type": "String",
#             "description": "A textual description explaining the purpose of the column."
#           }
#         }
#       }
#     }
#   },
#   "primaryKey": {
#     "type": "Array of Strings",
#     "description": "A list of column names that together make up the primary key of the table, ensuring each row is uniquely identifiable."
#   }
# }"""

# template_query_generater = ChatPromptTemplate.from_messages([
#     ("system"," You are an expert data steward and working as expert assistent to other member who want to use the Application. Application you use under the hood is Openmetadata, but when a user asks questions about the metadata of data or any question you cannot tell them about the application openmetadat. The main table useful for answering the user questions are below along with thier details Also the tag and tag_usage tables are used to find the tags and on which entities the tags are applied to, use this table to find the tags applied on different entities. <important> table = table_entity database = database_entity when user ask for table give the list of tables in table_entity when user ask for databases give the list of databases from database_entity </important> also <important> Please keep in mind that list of tables returned by the list_sql_database_tool tool is the list of table in the opentadata application db not from the data catalog user is aksing answers from. Please please use the table_entity to find the result of answer asked by user. </important> <important> entities are identified by their fqnHash </important>"),
#     ("system", "Given an input conversation, and relevent information about the database, tables, schema and relationships between the tables, create a syntactically correct mysql query to run on the database. Make sure the query is syntatically correct and returns sql. The sql you are generating is for openmetadata. The query should be correct and the answer should only containt the sql query without any special character. For the history of the conversation, please refer to the chat history. provided here"),
#     MessagesPlaceholder(variable_name="messages"),
#     ("system", """Question:  {question} List of all tables {tables}, list of revent tables {relevant_tables}, relevant tables schemas {relevant_tables_schemas}, <strong> Make sure you use only the tables in the list of tables provided to generate the query, <strong>also make sure you use table and columns specified in the schema, schema is in the json format described as this
        
#      {schema_description}
     
#      </strong> </strong> <strong> Please do not give the generic sql statements. Also if there is need to compare the data which contains the integers, you need to cast them to abs before comparing.</strong>"""),
# ])

# template_answer_user = ChatPromptTemplate.from_messages([
#     ("system", "Given the question, sql query, query result generate the final answer for the user. The answer should be like the answer given by the data steward In an organisation. If the query result is empty it means the database returned the empty result. You do not need to mention that you are answering the question based on the query result. You need to answer in the same way as the data steward would answer the question. You can also provide the answer to the question even if it is not the part of the query result. If the query result is empty do not provide fictional answer, answer accordingly as which entity not found or no relevent record found. The answer should be in the formrmal and polite tone."),
#     ("system", """  Question: 
#                     {question}  
#                     SQL Query:
#                     {sql_query}
#                     Query Result:
#                     {query_result}"""),
# ])

# template_query_checker = ChatPromptTemplate.from_messages([
#     ("system", "You are an MYSQL Expert and you can fix the query error and generate the correct query to run on the database. The query and query_error is given below. Also the detailed schema along with the descriptions in array format is given below, make sure you use table and columns specified in the schema, schema is in the json format. Please rewrite the query, check the query, and return the syntatically correct query to run on the database. Answer should only containt the sql query without any special character"),
#     ("system", """  query: 
#                     {query}  
#                     query_error:
#                     {query_error}
#                     schema:
#                     {relevant_tables_schemas}"""),
# ])


# # ListSQLDatabaseTool
# # Tool for getting tables names related to application, do not use it if user is asking for the table, for that you should query table_entity.
# def list_sql_database_tool(state: State):
#     """Tool for getting tables names.
#         Input is an empty string, output is a comma-separated list of tables in the database.

#         Get the question from the state and return the list of tables in the database.
#     """
#     state["tables"] = getListOfAllTables()
#     op = getListOfTables(state["question"])
#     state["relevant_tables"] = ", ".join(op["tables"])
#     state["relevant_tables_schemas"] = op["schemas"]
#     state["relevant_tables_relationships"] = str(getRelationshipsForTables(op["tables"]))
#     return state



# # InfoSQLDatabaseTool
# def info_sql_database_tool(state: State):
#     """Tool for getting metadata about a SQL database.
#         A comma-separated list of the table names for which to return the schema.
#         Example input: 'table1, table2, table3'
#         Get the schema and sample rows for the specified SQL tables."""
    
#     tableinfo = db.get_table_info_no_throw(
#             [t.strip() for t in state["relevant_tables"].split(",")]
#         )
    
#     state["query_error"] = ""
#     state["retry_count"] = 0
#     state["relevant_tables_sample_data"] = str(tableinfo)
#     return state

# # GenerateSQLQueryTool - 
# def generate_sql_query_tool(state: State):
#     """Tool for generating a SQL query.
#         Generate a SQL query based on the question and available information."""
#     input = {
#         "question": state["question"],
#         "tables": state["tables"],
#         "relevant_tables": state["relevant_tables"],
#         "relevant_tables_schemas": state["relevant_tables_schemas"],
#         # "relevant_tables_relationships": state["relevant_tables_relationships"],
#         # "relevant_tables_sample_data": state["relevant_tables_sample_data"],
#         "messages": state["messages"],
#         "schema_description": schema_description
#     }


#     chain = template_query_generater | model
#     output = chain.invoke(input)
#     sql_query = output.content
#     sql_query = sql_query.replace("sql\n", " ")
#     sql_query = sql_query.replace("\n", " ")
#     sql_query = sql_query.replace("```", " ")
#     state["sql_query"] = sql_query
#     state["query_error"] = ""
    
#     return state

# # QuerySQLDataBaseTool
# def query_sql_database_tool(state: State):
#     """Tool for querying a SQL database.
#         Input is a SQL query string, output is the result of the query.
#         Execute a SQL query against the database and get back the result..
#         If the query is not correct, an error message will be returned.
#         If an error is returned, rewrite the query, check the query, and try again."""
    
#     response = db.run_no_throw(state["sql_query"])
#     state["query_result"] = str(response)
    
#     state["retry_count"] = state["retry_count"] + 1
#     if "Error: " in state["query_result"] and state["retry_count"] < 3:
#         state["query_error"] = state["query_result"]
#     else:
#         state["query_error"] = ""
#     return state

# # QuerySQLCheckerTool
# def query_sql_checker_tool(state: State):
#     """Tool for checking a SQL query.
#         Input is a SQL query string, output is a boolean indicating whether the query is valid.
#         Check the syntax of a SQL query and return a boolean indicating whether the query is valid."""
    
#     input = {}
#     input["query"] = state["sql_query"]
#     input["query_error"] = state["query_error"]
#     input["relevant_tables_schemas"] = state["relevant_tables_schemas"]

#     chain = template_query_checker | model
#     output = chain.invoke(input)
#     sql_query = output.content
#     sql_query = sql_query.replace("sql\n", " ")
#     sql_query = sql_query.replace("\n", " ")
#     sql_query = sql_query.replace("```", " ")
#     state["sql_query"] = sql_query
#     state["query_error"] = ""
#     return state

# def generate_answer_for_user(state: State):
#     """Generate the final answer for the user.
#         Get the query result from the state and return it as the final answer."""
    
#     chain = template_answer_user | model

#     input = {
#         "question": state["question"],
#         "sql_query": state["sql_query"],
#         "tables": state["tables"],
#         "relevant_tables": state["relevant_tables"],
#         "relevant_tables_schemas": state["relevant_tables_schemas"],
#         "relevant_tables_relationships": state["relevant_tables_relationships"],
#         "relevant_tables_sample_data": state["relevant_tables_sample_data"],
#         "query_result": state["query_result"],
#     }
#     output = chain.invoke(input)
#     state["final_answer"] = output.content

#     state["messages"].append(HumanMessage(content=state["question"]))
#     state["messages"].append(AIMessage(content=state["final_answer"]))
    
#     return state



# # function to take user input and decide if it can be answered by sql query or not?
# def decide_query_or_not(state: State):
#     """Decide if the user query can be answered by a SQL query.
#         Check the user query and decide if it can be answered by a SQL query."""
    
#     state["messages"].append(HumanMessage(content=state["question"]))
#     state["messages"].append(SystemMessage(content="You are an expert data steward working on openmetadata system looking at the question asked by the user check if it can be answered by the query or not. State the answer in yes then reutrn only 'yes' as string, else answer the question of the user based on the history of the conversation."))
    
#     prompt = ChatPromptTemplate.from_messages(state["messages"])
#     chain = prompt | model
#     output = chain.invoke({})
#     response = output.content
#     if response == "yes":
#         state["is_query"] = "yes"
#     else:
#         state["is_query"] = "no"
#         state["messages"].pop()
#         state["messages"].append(AIMessage(content=response))

#     return state  