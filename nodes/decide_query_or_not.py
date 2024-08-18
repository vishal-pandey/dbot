from langchain_core.prompts import ChatPromptTemplate
from State import State
from models import model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


# function to take user input and decide if it can be answered by sql query or not?
def decide_query_or_not(state: State):
    """Decide if the user query can be answered by a SQL query.
        Check the user query and decide if it can be answered by a SQL query."""
    
    state["messages"].append(HumanMessage(content=state["question"]))
    state["messages"].append(SystemMessage(content="You are an expert data steward working on openmetadata system looking at the question asked by the user check if it can be answered by the query or not. State the answer in yes then reutrn only 'yes' as string, else answer the question of the user based on the history of the conversation."))
    
    prompt = ChatPromptTemplate.from_messages(state["messages"])
    chain = prompt | model
    output = chain.invoke({})
    response = output.content
    if response == "yes":
        state["is_query"] = "yes"
    else:
        state["is_query"] = "no"
        state["messages"].pop()
        state["messages"].append(AIMessage(content=response))

    return state  