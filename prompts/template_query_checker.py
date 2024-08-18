from langchain_core.prompts import ChatPromptTemplate

template_query_checker = ChatPromptTemplate.from_messages([
    ("system", "You are an MYSQL Expert and you can fix the query error and generate the correct query to run on the database. The query and query_error is given below. Also the detailed schema along with the descriptions in array format is given below, make sure you use table and columns specified in the schema, schema is in the json format. Please rewrite the query, check the query, and return the syntatically correct query to run on the database. Answer should only containt the sql query without any special character"),
    ("system", """  query: 
                    {query}  
                    query_error:
                    {query_error}
                    schema:
                    {relevant_tables_schemas}"""),
])