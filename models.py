from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)