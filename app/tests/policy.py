def test_create_policy(client):
    response = client.post("/api/v1/policies", json={
        "name": "Policy 1",
        "days_allowed": 10,
        "policy_type": "Annual"
    })
    assert response.status_code == 200

def test_duplicate_policy_name_fails(client):
    client.post("/api/v1/policies", json={
        "name": "Policy 1",
        "days_allowed": 10,
        "policy_type": "Annual"
    })
    # Try to create another policy with same name
    response = client.post("/api/v1/policies", json={
        "name": "Policy 1",
        "days_allowed": 10,
        "policy_type": "Annual"
    })
    assert response.status_code == 400

def test_duplicate_policy(client):
    client.post("/api/v1/policies", json={
        "name": "Policy 1",
        "days_allowed": 10,
        "policy_type": "Annual"
    })
    response = client.get("/api/v1/policies/1/duplicate")
    assert response.status_code == 200

def test_get_policies(client):
    # Seed policies
    client.create_policies(15)
    response = client.get("/api/v1/policies", params={"skip": 0, "limit": 10})
    json_data = response.json()['data']

    # assert that the json_data is 10 items only
    assert len(json_data) == 10
    
    # move to the next page
    response = client.get("/api/v1/policies", params={"skip": 10, "limit": 10})
    json_data = response.json()['data']
    assert len(json_data) == 5

    
# - Duplicating a policy creates correct copy
# - Pagination works correctly
# - Invalid date ranges are rejected
# - Soft delete doesn't actually remove record
# - Edge cases (empty strings, null values, etc.)
