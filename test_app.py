import pytest

from app import app, books  # Import necessary objects

# Test fixture to add some sample books before each test
@pytest.fixture
def sample_books():
    books.clear()  # Clear existing books
    books.extend([
        {"id": 1, "title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams"},
        {"id": 2, "title": "Pride and Prejudice", "author": "Jane Austen"},
    ])

# Test for the base route (`/`) with GET request
def test_index_get(client, sample_books):
    response = client.get("/")
    assert response.status_code == 200  # Check for successful response
    assert b"Book List" in response.data  # Check for presence of "Book List" in the rendered template

# Test for the base route (`/`) with POST request (empty search)
def test_index_post_empty_search(client, sample_books):
    response = client.post("/", data={"query": ""})
    assert response.status_code == 200
    assert len(response.json) == 2  # Check if all books are returned

# Test for the base route (`/`) with POST request (matching search)
def test_index_post_search(client, sample_books):
    response = client.post("/", data={"query": "Adams"})
    assert response.status_code == 200
    assert len(response.json) == 1  # Check if only matching book is returned (Hitchhiker's Guide)

# Test for adding a new book
def test_add_book(client):
    data = {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"}
    response = client.post("/add-book", data=data)
    assert response.status_code == 302  # Check for redirect
    assert len(books) == 3  # Check if a new book was added

# Test for editing a book that exists
def test_edit_book_existing(client, sample_books):
    data = {"title": "The Martian", "author": "Andy Weir"}
    response = client.post("/edit-book/1", data=data)
    assert response.status_code == 302
    assert books[0]["title"] == "The Martian"  # Check if the first book's title was updated

# Test for editing a book that doesn't exist
def test_edit_book_nonexistent(client):
    data = {"title": "Nonexistent Book", "author": "Unknown"}
    response = client.post("/edit-book/99", data=data)
    assert response.status_code == 404  # Check for 404 Not Found

# Test for deleting a book
def test_delete_book(client, sample_books):
    response = client.post("/delete-book/2", follow_redirects=True)
    assert response.status_code == 200
    assert len(books) == 1  # Check if book with ID 2 was removed
