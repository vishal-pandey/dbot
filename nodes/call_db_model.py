

# Node to generate the answer as sql and execute and send the result to the user.
from toolkits.SQLDatabaseToolkit import SQLDatabaseToolkit
from databases import db
from models import model
from State import State



def call_db_model(state: State):
    sqltoolkit = SQLDatabaseToolkit(db=db, llm=model, state=state)
    dbtools = sqltoolkit.get_tools()

    model_db = model.bind_tools(dbtools)
    response = model_db.invoke(state["messages"])

    return {"messages": response}