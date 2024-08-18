from State import State
from databases import db
from models import model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from prompts import template_answer_user

def generate_answer_for_user(state: State):
    """Generate the final answer for the user.
        Get the query result from the state and return it as the final answer."""
    
    chain = template_answer_user | model

    input = {
        "question": state["question"],
        "sql_query": state["sql_query"],
        "tables": state["tables"],
        "relevant_tables": state["relevant_tables"],
        "relevant_tables_schemas": state["relevant_tables_schemas"],
        "relevant_tables_relationships": state["relevant_tables_relationships"],
        "relevant_tables_sample_data": state["relevant_tables_sample_data"],
        "query_result": state["query_result"],
    }
    output = chain.invoke(input)
    state["final_answer"] = output.content

    state["messages"].append(HumanMessage(content=state["question"]))
    state["messages"].append(AIMessage(content=state["final_answer"]))
    
    return state
