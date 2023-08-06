# test_hello.py
from app.hello import app

def test_hello():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello, World!'

def test_greet():
    response = app.test_client().get('/greet')

    assert response.status_code == 200
    assert response.data == b'greetings'
