<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>Library Management System</h1>

<p>This project is a simple Library Management System built using <strong>Flask</strong>, a Python-based web framework. It allows users to add, edit, delete, and search books. The data is temporarily stored in memory and is not persistent beyond the application's runtime.</p>

<h2>Table of Contents</h2>
<ol>
    <li><a href="#how-to-run-the-project">How to Run the Project</a></li>
    <li><a href="#design-choices">Design Choices</a></li>
    <li><a href="#assumptions-and-limitations">Assumptions and Limitations</a></li>
    <li><a href="#data-structure-used">Data Structure Used</a></li>
    <li><a href="#test-cases">Test Cases</a></li>
    <li><a href="#other-considerations">Other Considerations</a></li>
</ol>

<h2 id="how-to-run-the-project">How to Run the Project</h2>

<h3>Prerequisites</h3>
<p>Ensure you have the following installed:</p>
<ul>
    <li>Python 3.7 or later</li>
    <li><code>pip</code> for installing Python packages</li>
</ul>

<h3>Installation</h3>
<ol>
    <li>Clone the repository:
        <pre><code>git clone https://github.com/NSAjay2279/Library-Management-System.git<repository_url>
cd Library-Management-System<project_directory></code></pre>
    </li>
    <li>Create and activate a virtual environment:
        <pre><code>python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`</code></pre>
    </li>
    <li>Install required dependencies:
        <pre><code>pip install -r requirements.txt</code></pre>
        If you don’t have a <code>requirements.txt</code>, you can install Flask manually:
        <pre><code>pip install flask pytest</code></pre>
    </li>
</ol>

<h3>Running the Application</h3>
<ol>
    <li>Start the Flask development server:
        <pre><code>flask run</code></pre>
    </li>
    <li>Open your browser and go to <a href="http://127.0.0.1:5000/">http://127.0.0.1:5000/</a> to interact with the Library Management System.</li>
</ol>

<h3>Running Tests</h3>
<p>To run the test cases, use <code>pytest</code>:</p>
<pre><code>pytest</code></pre>
<p>This will automatically discover and run all the test functions defined in the project.</p>

<h2 id="design-choices">Design Choices</h2>

<ul>
    <li><strong>Flask Framework</strong>: Flask was chosen for its simplicity and flexibility, allowing easy integration of routes and templates.</li>
    <li><strong>In-Memory Storage</strong>: For simplicity and testing purposes, an in-memory list of dictionaries is used to store books. Each book has an <code>id</code>, <code>title</code>, and <code>author</code>. This allows for quick testing without involving a database.</li>
    <li><strong>HTML Templates</strong>: Jinja2 templating engine (integrated with Flask) is used to render dynamic content in HTML files. The <code>layout.html</code> file is the base template, and other pages extend this base to avoid code duplication.</li>
    <li><strong>RESTful Routing</strong>: The app uses RESTful routes for different functionalities like adding, editing, deleting, and searching books. These routes follow conventional HTTP methods like GET, POST, and DELETE.</li>
    <li><strong>Separation of Concerns</strong>: Logic for handling the book data is separated from the presentation layer (HTML templates). This makes it easier to scale the application if needed.</li>
</ul>

<h2 id="assumptions-and-limitations">Assumptions and Limitations</h2>

<h3>Assumptions</h3>
<ul>
    <li><strong>Basic Features</strong>: The app only supports basic book management (add, edit, delete, search) and does not implement advanced features like user authentication or persistent data storage.</li>
    <li><strong>In-Memory Data</strong>: Data is stored temporarily in memory, meaning that the book list is cleared every time the server is restarted.</li>
</ul>

<h3>Limitations</h3>
<ul>
    <li><strong>No Persistent Storage</strong>: As mentioned, the app uses in-memory storage, which means that once the server is restarted, all data is lost. To add persistence, a database like SQLite or PostgreSQL can be integrated.</li>
    <li><strong>Basic Search Functionality</strong>: The search functionality is rudimentary, only searching by title or author and not considering partial or fuzzy matches.</li>
    <li><strong>No User Management</strong>: The system does not have any user login or roles (e.g., admin vs. regular user).</li>
</ul>

<h2 id="data-structure-used">Data Structure Used</h2>

<p>The books are stored in a list of dictionaries where each dictionary represents a book with the keys <code>id</code>, <code>title</code>, and <code>author</code>.</p>

<pre><code>
books = [
    {'id': 1, 'title': 'Book Title 1', 'author': 'Author 1'},
    {'id': 2, 'title': 'Book Title 2', 'author': 'Author 2'}
]
</code></pre>

<h3>Why This Data Structure?</h3>
<ul>
    <li><strong>List of Dictionaries</strong>: Using a list allows easy iteration over all books. Dictionaries are chosen for their easy key-value structure, making it simple to store and access book attributes like <code>title</code> and <code>author</code>.</li>
    <li><strong>Scalability</strong>: This approach is fine for small-scale or prototype applications. However, for larger systems, a database or more efficient data structure may be required.</li>
</ul>

<h2 id="test-cases">Test Cases</h2>

<h3>Overview</h3>
<p>The <code>pytest</code> framework is used to define test cases for the app. The provided tests include basic functionality such as:</p>
<ul>
    <li>Displaying books (<code>test_display_books</code>)</li>
    <li>Searching books (<code>test_search_books</code>)</li>
    <li>Adding a new book (<code>test_add_book</code>)</li>
</ul>

<h3>Missing Test Cases</h3>
<ul>
    <li><strong>Edit Book</strong>: You can add a test for editing a book's details, such as changing its title or author.</li>
    <li><strong>Delete Book</strong>: A test to ensure that books can be successfully deleted from the list.</li>
    <li><strong>Edge Cases</strong>: Tests for invalid inputs, such as empty fields, duplicate book entries, or invalid search queries.</li>
    <li><strong>Search Results</strong>: Ensure that the search is case-insensitive and returns the correct results.</li>
</ul>

<h3>Example Test Case for Editing a Book</h3>
<pre><code>
def test_edit_book(client):
    # First, add a book to ensure there is a book to edit
    client.post('/add-book', data={'title': 'Original Title', 'author': 'Author Name'})
    
    # Edit the book
    response = client.post('/edit-book/1', data={'title': 'Updated Title', 'author': 'Updated Author'})
    
    assert response.status_code == 302  # Assuming a redirect after successful edit
    assert b'Updated Title' in response.data  # Check if the updated title is shown
</code></pre>

<h2 id="other-considerations">Other Considerations</h2>

<ul>
    <li><strong>UI/UX</strong>: The current user interface is minimal. You may want to enhance it with CSS frameworks like <strong>Bootstrap</strong> for a better user experience.</li>
    <li><strong>Future Enhancements</strong>: 
        <ul>
            <li>Integrate a database to store books persistently.</li>
            <li>Implement user authentication and role-based access.</li>
            <li>Implement a better search feature using full-text search.</li>
            <li>Use <strong>AJAX</strong> for dynamically updating the book list without reloading the page.</li>
        </ul>
    </li>
</ul>

<p>Feel free to modify and extend the README based on the project’s evolving requirements. If you need any further help, feel free to reach out!</p>

</body>
</html>
