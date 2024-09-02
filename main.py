from Graph import Graph
from State import State
from langchain_core.messages import HumanMessage, SystemMessage
import chainlit as cl
import random
from prompts.prompt_ai import get_prompt_ai
from prompts.prompt_info_db import get_prompt_info_db

config = {"configurable": {"thread_id": "4"}}

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)


inputs:State = {}



@cl.on_chat_start
async def main():
    print("IT is called being called")
    config["configurable"]["thread_id"] = str(int(random.random()*10000000))

@cl.on_message
async def main(message: cl.Message):

    final_answer = await cl.Message(content="").send()

    f = 0
    inputs["question"] = message.content
    if f == 0:
        f = 1
        inputs["messages"] = [get_prompt_ai(question=message.content), HumanMessage(content=message.content)]
        # inputs["temp_messages"] = [get_prompt_info_db(message.content)]
    else:
        inputs["messages"] = [HumanMessage(content=message.content)]


    async for event in Graph.astream_events(inputs, config, stream_mode="values", version="v2"):
        if event["event"] == "on_chat_model_stream" and event["name"] == "ChatOpenAI" and event["metadata"]["langgraph_node"] != "generate_sql_query_tool":
        # if event["event"] == "on_chat_model_stream" and event["name"] == "ChatOpenAI" and event["metadata"]["langgraph_node"] != "generate_question_node" and event["metadata"]["langgraph_node"] != "tools":
            content = event["data"]["chunk"].content or ""
            await final_answer.stream_token(token=content)
    await final_answer.update()


