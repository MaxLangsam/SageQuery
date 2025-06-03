import os
import csv
import argparse
from tqdm import tqdm

# Embedding backends
try:
    import openai
except ImportError:
    openai = None
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

# Vector DBs
try:
    import pinecone
except ImportError:
    pinecone = None
try:
    import psycopg2
except ImportError:
    psycopg2 = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PGVECTOR_URL = os.getenv("PGVECTOR_URL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "sagequery-index")
DATASET_PATH = os.getenv("DATASET_PATH", "sql-create-context.csv")


def embed_openai(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def embed_hf(text, model):
    return model.encode(text).tolist()

def load_dataset(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prompt = row["prompt"]
            # Split the prompt into question and SQL parts
            # The format appears to be <|system|>\nSQL_QUERY\n<|user|>\nQUESTION
            parts = prompt.split("<|user|>")
            if len(parts) == 2:
                sql_part = parts[0].replace("<|system|>\n", "").strip()
                question = parts[1].strip()
                yield question, sql_part

def insert_pgvector(pairs, embed_fn):
    conn = psycopg2.connect(PGVECTOR_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sql_examples (
            id SERIAL PRIMARY KEY,
            question TEXT,
            sql TEXT,
            embedding VECTOR(1536)
        );
    """)
    for question, sql in tqdm(pairs):
        emb = embed_fn(question)
        cur.execute(
            "INSERT INTO sql_examples (question, sql, embedding) VALUES (%s, %s, %s)",
            (question, sql, emb)
        )
    conn.commit()
    cur.close()
    conn.close()

def insert_pinecone(pairs, embed_fn):
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    if PINECONE_INDEX not in pinecone.list_indexes():
        pinecone.create_index(PINECONE_INDEX, dimension=1536)
    index = pinecone.Index(PINECONE_INDEX)
    batch = []
    for i, (question, sql) in enumerate(tqdm(pairs)):
        emb = embed_fn(question)
        batch.append((f"ex-{i}", emb, {"question": question, "sql": sql}))
        if len(batch) >= 100:
            index.upsert(batch)
            batch = []
    if batch:
        index.upsert(batch)

def main():
    parser = argparse.ArgumentParser(description="Embed and load SQL examples into vector DB.")
    parser.add_argument('--backend', choices=['openai', 'hf'], default='openai', help='Embedding backend')
    parser.add_argument('--vectordb', choices=['pgvector', 'pinecone'], default='pgvector', help='Vector DB backend')
    parser.add_argument('--hf-model', default='all-MiniLM-L6-v2', help='HuggingFace model name')
    args = parser.parse_args()

    pairs = list(load_dataset(DATASET_PATH))

    if args.backend == 'openai':
        if not openai:
            raise ImportError('openai package not installed')
        openai.api_key = OPENAI_API_KEY
        embed_fn = embed_openai
    else:
        if not SentenceTransformer:
            raise ImportError('sentence-transformers package not installed')
        model = SentenceTransformer(args.hf_model)
        embed_fn = lambda text: embed_hf(text, model)

    if args.vectordb == 'pgvector':
        if not psycopg2:
            raise ImportError('psycopg2 package not installed')
        insert_pgvector(pairs, embed_fn)
    else:
        if not pinecone:
            raise ImportError('pinecone-client package not installed')
        insert_pinecone(pairs, embed_fn)

if __name__ == "__main__":
    main() 