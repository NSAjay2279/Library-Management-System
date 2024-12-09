import pytest
from app import app, books


@pytest.fixture
def client():
    # Setup the Flask test client
    with app.test_client() as client:
        yield client
    # Cleanup after tests
    books.clear()


def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    # Assuming title in `index.html`
    assert b"Library Management System" in response.data


def test_add_book(client):
    # Add a book via POST request
    response = client.post(
        '/add-book', data={'title': 'Test Book', 'author': 'Test Author'})
    assert response.status_code == 302  # Redirect after adding a book
    assert len(books) == 1
    assert books[0]['title'] == 'Test Book'
    assert books[0]['author'] == 'Test Author'


def test_edit_book(client):
    # Add a book for editing
    books.append({'id': 1, 'title': 'Old Title', 'author': 'Old Author'})

    # Edit the book via POST request
    response = client.post(
        '/edit-book/1', data={'title': 'New Title', 'author': 'New Author'})
    assert response.status_code == 302  # Redirect after editing
    assert books[0]['title'] == 'New Title'
    assert books[0]['author'] == 'New Author'


def test_edit_book_not_found(client):
    response = client.get('/edit-book/99')
    assert response.status_code == 404  # Book not found


def test_delete_book(client):
    # Add a book to delete
    books.append({'id': 1, 'title': 'Book to Delete', 'author': 'Author'})

    # Delete the book via POST request
    response = client.post('/delete-book/1')
    assert response.status_code == 302  # Redirect after deleting
    assert len(books) == 0


def test_search_books(client):
    # Add some books for searching
    books.extend([
        {'id': 1, 'title': 'Python 101', 'author': 'John Doe'},
        {'id': 2, 'title': 'Flask Guide', 'author': 'Jane Smith'}
    ])

    # Search for books
    response = client.post('/', data={'query': 'python'})
    assert response.status_code == 200
    assert b"Python 101" in response.data
    assert b"John Doe" in response.data
    assert b"Flask Guide" not in response.data
