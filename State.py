from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from models import model
from databases import db



class State(TypedDict):
    model = model
    db = db

    question: str
    sql_query: str
    tables: str
    relevant_tables: str
    relevant_tables_schemas: str
    relevant_tables_relationships: str
    relevant_tables_sample_data: str
    query_error: str
    retry_count: int

    query_result: str
    final_answer: str
    messages: Annotated[list[AnyMessage], add_messages]