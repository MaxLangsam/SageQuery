import pytest
from backend.services.nl2sql import nl_to_sql_service

def test_nl_to_sql_service_basic():
    question = "List all users."
    examples = [{"question": "Show all users.", "sql": "SELECT * FROM users;"}]
    sql = nl_to_sql_service(question, examples, schema="users(id, name)")
    assert "SELECT" in sql.upper() 