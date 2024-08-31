import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import chromadb
import json
chroma_client = chromadb.Client()


f = open("dbinfo.json", "r")
dbinfo = json.loads(f.read())

f = open("dbrelationships.json", "r")
dbrelationships = json.loads(f.read())


ids = []
documents = []
for table in dbinfo["tables"]:
    ids.append(table['name'])
    documents.append(str(table))


import chromadb.utils.embedding_functions as embedding_functions
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
collection = chroma_client.create_collection(name="my_collection", embedding_function=openai_ef)


collection.add(
    documents=documents,
    ids=ids
)

def getListOfAllTables() -> str:
    return ",".join(ids)

def getListOfTables(query) -> str:
    results = collection.query(
        query_texts=[query], # Chroma will embed this for you
        n_results=5 # how many results to return
    )
    tables = results['ids'][0]
    documents = results['documents'][0]
    op = {
        "tables": tables,
        "schemas": documents
    }
    return op

def getRelationshipsForTables(tables):
    allrelationships = dbrelationships['relationships']
    relationships = []
    for rel in allrelationships:
        if (rel['fromTable'] in tables or rel['toTable'] in tables):
            relationships.append(rel)
    
    return str(relationships)

def getShcemaForTables(tables):
    schemas = []
    for table in tables:
        for t in dbinfo["tables"]:
            if t['name'] == table:
                schemas.append(t)
    return str(schemas)