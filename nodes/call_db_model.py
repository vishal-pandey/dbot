

# Node to generate the answer as sql and execute and send the result to the user.
from toolkits.SQLDatabaseToolkit import SQLDatabaseToolkit
from databases import db
from models import model
from State import State
from prompts.prompt_info_db import get_prompt_info_db


def call_db_model(state: State):
    sqltoolkit = SQLDatabaseToolkit(db=db, llm=model)
    dbtools = sqltoolkit.get_tools()

    model_db = model.bind_tools(dbtools)
    response = model_db.invoke(state["messages"])

    return {"messages": response}


def call_db_info_model(state: State):
    sqltoolkit = SQLDatabaseToolkit(db=db, llm=model)
    dbtools = sqltoolkit.get_less_tools()

    model_db = model.bind_tools(dbtools)

    # state["temp_messages"].append(get_prompt_info_db(state["question"]))
    response = model_db.invoke(state["temp_messages"])

    return {"temp_messages": response}

def trasfer_temp_to_messages(state: State):
    return {"messages": state["temp_messages"][-1]}