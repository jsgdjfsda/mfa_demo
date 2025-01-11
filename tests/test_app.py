import pytest
from app import app, MFADemo
import json
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mfa_demo(tmpdir):
    storage_file = os.path.join(tmpdir, "test_devices.json")
    return MFADemo(storage_file=storage_file)

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_register_device(client):
    response = client.post('/register',
                          data=json.dumps({'username': 'testuser'}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'qr_code' in data

def test_verify_code_unregistered_user(client):
    response = client.post('/verify',
                          data=json.dumps({
                              'username': 'nonexistent',
                              'code': '123456'
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'User not registered' in data['message']

def test_mfa_demo_initialization(mfa_demo):
    assert mfa_demo.devices == {}
