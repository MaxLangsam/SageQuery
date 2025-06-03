import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import re

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

DANGEROUS_SQL = re.compile(r"\b(drop|delete|truncate|alter|update|insert)\b", re.IGNORECASE)

def execute_sql_service(sql: str):
    # Prevent dangerous queries
    if DANGEROUS_SQL.search(sql):
        raise ValueError("Dangerous SQL detected. Only SELECT queries are allowed.")
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
        return rows
    except SQLAlchemyError as e:
        raise ValueError(f"SQL execution error: {str(e)}") 