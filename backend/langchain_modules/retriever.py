import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone, PGVector
from langchain.schema import BaseRetriever

VECTOR_DB = os.getenv("VECTOR_DB", "pinecone")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "sagequery-index")
PGVECTOR_URL = os.getenv("PGVECTOR_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ExampleRetriever(BaseRetriever):
    def __init__(self, k=3):
        self.k = k
        self.embedder = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")
        if VECTOR_DB == "pinecone":
            self.db = Pinecone(index_name=PINECONE_INDEX, embedding_function=self.embedder)
        else:
            self.db = PGVector(connection_string=PGVECTOR_URL, embedding_function=self.embedder)

    def get_relevant_examples(self, query: str):
        query_embedding = self.embedder.embed_query(query)
        results = self.db.similarity_search_by_vector(query_embedding, k=self.k)
        return [{"question": r.metadata["question"], "sql": r.metadata["sql"]} for r in results] 