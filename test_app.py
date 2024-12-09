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

    # Extract book ID from the response (adjust based on your template/redirect behavior)
    book_id = extract_book_id_from_response(
        response)  # Implement this function

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

    # Extract book ID from the response (adjust based on your template/redirect behavior)
    book_id = extract_book_id_from_response(
        response)  # Implement this function

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

# Implement this function to extract book ID from response


def extract_book_id_from_response(response):
    # Example: If your template redirects to a URL with the book ID
    if 'Location' in response.headers:
        url = response.headers['Location']
        book_id = int(url.split('/')[-1])
        return book_id

    # Example: If your template displays the book ID in the response content
    book_id_pattern = r'Book ID: (\d+)'
    match = re.search(book_id_pattern, response.data.decode('utf-8'))
    if match:
        return int(match.group(1))

    # Adjust this function based on your specific template/redirect behavior
    raise ValueError("Could not extract book ID from response")


if __name__ == '__main__':
    pytest.main()
