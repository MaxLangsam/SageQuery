import requests
import pytest

API_URL = "http://localhost:8000"

@pytest.mark.order(1)
def test_nl_to_sql_and_results():
    question = "List all users"
    resp = requests.post(f"{API_URL}/query/", json={"question": question})
    assert resp.status_code == 200
    data = resp.json()
    assert "select" in data["sql"].lower()
    assert isinstance(data.get("results", []), list)
    assert isinstance(data.get("grounded_examples", []), list)

@pytest.mark.order(2)
def test_schema_discovery():
    resp = requests.get(f"{API_URL}/schema/")
    assert resp.status_code == 200
    schema = resp.json()
    assert isinstance(schema, dict)
    assert all(isinstance(cols, list) for cols in schema.values())

@pytest.mark.order(3)
def test_vector_grounding():
    question = "Show all orders"
    resp = requests.post(f"{API_URL}/query/", json={"question": question, "preview": True})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data.get("grounded_examples", []), list)

@pytest.mark.order(4)
def test_safe_query_execution():
    # Dangerous query should be blocked
    resp = requests.post(f"{API_URL}/query/", json={"question": "DROP TABLE users;"})
    assert resp.status_code == 400 or resp.status_code == 200
    if resp.status_code == 200:
        # Should not return results for dangerous SQL
        data = resp.json()
        assert not data.get("results")

@pytest.mark.order(5)
def test_feedback_submission():
    feedback = {
        "question": "List all users",
        "sql": "SELECT * FROM users;",
        "feedback": "Works great!",
        "correct": True
    }
    resp = requests.post(f"{API_URL}/feedback/", json=feedback)
    assert resp.status_code == 200
    assert resp.json()["status"] == "success" 