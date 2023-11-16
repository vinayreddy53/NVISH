# Unit Testing Code:

import pytest
from exercise4 import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_save_endpoint(client):
    # Test save endpoint
    data = {'key': 'test_key', 'value': 'test_value'}
    response = client.post('/save', json=data)
    assert response.status_code == 200
    assert b'Data saved successfully' in response.data

def test_get_endpoint(client):
    # Test get endpoint
    response = client.get('/get/test_key')
    assert response.status_code == 200
    assert b'test_key' in response.data
    assert b'test_value' in response.data

def test_delete_endpoint(client):
    # Test delete endpoint
    response = client.delete('/delete/test_key')
    assert response.status_code == 200
    assert b'Data deleted successfully' in response.data
  
# End-to-End Testing:

import requests

def test_full_workflow():
    # Test the complete workflow - saving, getting, and deleting
    data = {'key': 'e2e_key', 'value': 'e2e_value'}

    # Save data
    save_response = requests.post('http://127.0.0.1:5000/save', json=data)
    assert save_response.status_code == 200
    assert save_response.json()['message'] == 'Data saved successfully'

    # Get data
    get_response = requests.get('http://127.0.0.1:5000/get/e2e_key')
    assert get_response.status_code == 200
    assert get_response.json()['key'] == 'e2e_key'
    assert get_response.json()['value'] == 'e2e_value'

    # Delete data
    delete_response = requests.delete('http://127.0.0.1:5000/delete/e2e_key')
    assert delete_response.status_code == 200
    assert delete_response.json()['message'] == 'Data deleted successfully'


