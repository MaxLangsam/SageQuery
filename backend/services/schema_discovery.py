import os
from sqlalchemy import create_engine, inspect

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def get_schema_service():
    inspector = inspect(engine)
    schema = {}
    for table_name in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns(table_name)]
        schema[table_name] = columns
    return schema 