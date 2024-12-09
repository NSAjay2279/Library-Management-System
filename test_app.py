import pytest
from app import app  # Assuming your app is in a file named app.py


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_display_books(client):
    response = client.get('/')
    assert response.status_code == 200
    # Assert that the book list is present in the response


def test_search_books(client):
    # Simulate a search query
    response = client.post('/', data={'query': 'python'})
    assert response.status_code == 200
    # Assert that the search results are displayed correctly


def test_add_book(client):
    # Simulate adding a new book
    response = client.post(
        '/add-book', data={'title': 'Test Book', 'author': 'Test Author'})
    assert response.status_code == 302  # Assuming redirect after adding
    # Assert that the new book is displayed in the book list

# ... similar tests for editing and deleting books
