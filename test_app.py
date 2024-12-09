import unittest
from app import app


class TestIndexRoute(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_get_index(self):
        # Test GET request
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Welcome to the Library Management System', response.data)

    def test_post_search_books_found(self):
        # Test POST request with a query that matches a book
        # Assuming `books` is defined globally in app.py for simplicity
        global books
        books = [
            {"id": 1, "title": "Python Programming", "author": "John Doe"},
            {"id": 2, "title": "Flask Development", "author": "Jane Smith"}
        ]

        response = self.app.post('/', data={'query': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python Programming', response.data)
        self.assertIn(b'Search Results for "python"', response.data)

    def test_post_search_books_not_found(self):
        # Test POST request with a query that doesn't match any books
        global books
        books = [
            {"id": 1, "title": "Python Programming", "author": "John Doe"},
            {"id": 2, "title": "Flask Development", "author": "Jane Smith"}
        ]

        response = self.app.post('/', data={'query': 'Java'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Results for "java"', response.data)
        self.assertIn(b'Not Found', response.data)


if __name__ == '__main__':
    unittest.main()
