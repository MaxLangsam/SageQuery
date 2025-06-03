import os
from openai import OpenAI
from langchain.vectorstores import Pinecone, PGVector
from langchain.embeddings import OpenAIEmbeddings

VECTOR_DB = os.getenv("VECTOR_DB", "pinecone")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "sagequery-index")
PGVECTOR_URL = os.getenv("PGVECTOR_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Assume examples are already embedded and stored in the vector DB

def rag_grounding_service(question: str, k: int = 3):
    embedder = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    query_embedding = embedder.embed_query(question)
    if VECTOR_DB == "pinecone":
        db = Pinecone(index_name=PINECONE_INDEX, embedding_function=embedder)
    else:
        db = PGVector(connection_string=PGVECTOR_URL, embedding_function=embedder)
    results = db.similarity_search_by_vector(query_embedding, k=k)
    # Each result is a dict with 'question' and 'sql'
    return [{"question": r.metadata["question"], "sql": r.metadata["sql"]} for r in results] 