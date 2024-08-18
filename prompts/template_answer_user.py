from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

template_answer_user = ChatPromptTemplate.from_messages([
    ("system", "Given the question, sql query, query result generate the final answer for the user. The answer should be like the answer given by the data steward In an organisation. If the query result is empty it means the database returned the empty result. You do not need to mention that you are answering the question based on the query result. You need to answer in the same way as the data steward would answer the question. You can also provide the answer to the question even if it is not the part of the query result. If the query result is empty do not provide fictional answer, answer accordingly as which entity not found or no relevent record found. The answer should be in the formrmal and polite tone."),
    ("system", """  Question: 
                    {question}  
                    SQL Query:
                    {sql_query}
                    Query Result:
                    {query_result}"""),
])
