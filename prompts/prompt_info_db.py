from langchain_core.messages import SystemMessage, HumanMessage

# from dbragtool import getListOfTables


def get_prompt_info_db(question:str):

    prompt_info_db = HumanMessage(content=f"""
            I have a question which I want to answer using the data catalog, question is below
            Question: {question}
            I am using data OpenMetadata as the data catalog.
            I have the database of the openmetadata where all the metadata about the data is stored.
            
            You have access to the following tools, explained below.

            list_sql_database_tool: To list the tables available in the database
            relationship_fetch_tool: To fetch the relationships between the tables
            schema_fetch_tool: To fetch the schema of the tables

            Use the above provided tables and give me strategy to build the query to answer the question, the strategy should contains which tables and which columns of those table is relevent for getting the answer.
            <important> table in the question is not about the table of the openemetadata, it is about the ingested tables in the openmetadata catalog which is present in the table_entity table </important
            Please fetch the schema of the relevent tables from the relationships also there might be data available to answer the question from the related tables also.
        """)
    return prompt_info_db

