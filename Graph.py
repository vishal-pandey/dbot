import asyncio
from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver
from GraphBuilder import GraphBuilder

memory = AsyncSqliteSaver.from_conn_string("mymemory.db")
# memory = SqliteSaver.from_conn_string("mymemory.db")


Graph = GraphBuilder.compile(checkpointer=memory)
