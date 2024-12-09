import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_edit_book(client):
    # Add a new book first
    response = client.post(
        '/add-book', data={'title': 'Test Book', 'author': 'Test Author'})
    book_id = response.headers['Location'].split('/')[-1]

    # Edit the book
    response = client.post(
        f'/edit-book/{book_id}', data={'title': 'Updated Title', 'author': 'Updated Author'})
    assert response.status_code == 302

    # Verify the update
    response = client.get('/')
    assert 'Updated Title' in response.data.decode()


def test_delete_book(client):
    # Add a new book first
    response = client.post(
        '/add-book', data={'title': 'Test Book', 'author': 'Test Author'})
    book_id = response.headers['Location'].split('/')[-1]

    # Delete the book
    response = client.post(f'/delete-book/{book_id}')
    assert response.status_code == 302

    # Verify the deletion
    response = client.get('/')
    assert 'Test Book' not in response.data.decode()
