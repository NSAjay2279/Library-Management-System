import pytest
from app import app  # Assuming your app is in a file named app.py
from flask import url_for


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_edit_book_successful(client):
    # Add a book
    response = client.post(
        '/add-book', data={'title': 'Test Book', 'author': 'Test Author'})
    assert response.status_code == 302

    # Get the book ID from the redirect URL
    book_id = int(response.headers['Location'].split('/')[-1])

    # Access edit page
    response = client.get(f'/edit-book/{book_id}')
    assert response.status_code == 200

    # Modify book details
    new_title = "Updated Title"
    new_author = "Updated Author"
    response = client.post(
        f'/edit-book/{book_id}', data={'title': new_title, 'author': new_author})
    assert response.status_code == 302

    # Check updated book details on index
    response = client.get('/')
    assert new_title in response.data.decode('utf-8')
    assert new_author in response.data.decode('utf-8')


def test_edit_book_nonexistent(client):
    response = client.get('/edit-book/999')  # Non-existent ID
    assert response.status_code == 404


def test_delete_book_successful(client):
    # Add a book
    response = client.post(
        '/add-book', data={'title': 'Test Book', 'author': 'Test Author'})
    assert response.status_code == 302

    # Get the book ID from the redirect URL
    book_id = int(response.headers['Location'].split('/')[-1])

    # Check book presence before deletion
    response = client.get('/')
    assert "Test Book" in response.data.decode('utf-8')

    # Delete the book
    response = client.post(f'/delete-book/{book_id}')
    assert response.status_code == 302

    # Check book absence after deletion
    response = client.get('/')
    assert "Test Book" not in response.data.decode('utf-8')


def test_delete_book_nonexistent(client):
    response = client.post('/delete-book/999')  # Non-existent ID
    assert response.status_code == 404

# Add more test cases as needed, such as:
# - Editing a book with invalid input
# - Deleting the last book
# - Editing a book with special characters
# - Mass deletion of books
# - Performance testing
# - Security testing


if __name__ == '__main__':
    pytest.main()
