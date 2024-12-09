from flask import Flask, request, render_template, redirect, url_for
from typing import List, Dict, Optional

app = Flask(__name__)

# Temporary in-memory storage for books
books: List[Dict[str, Optional[str]]] = []

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    query = None
    results = None

    if request.method == 'POST':
        query = request.form.get('query', '').lower()
        if query:
            results = [book for book in books if query in book['title'].lower().split() or query in book['author'].lower().split()]

    return render_template('index.html', books=books, query=query, results=results)

@app.route('/add-book', methods=['GET', 'POST'])
def add_book() -> str:
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        books.append({'id': len(books) + 1, 'title': title, 'author': author})
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id: int) -> str:
    book = next((b for b in books if b['id'] == book_id), None)
    
    if book is None:
        return "Book not found", 404  # Return a 404 error if the book doesn't exist
    
    if request.method == 'POST':
        book['title'] = request.form['title']
        book['author'] = request.form['author']
        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book)

@app.route('/delete-book/<int:book_id>', methods=['POST'])
def delete_book(book_id: int) -> str:
    global books
    books = [book for book in books if book['id'] != book_id]  # Remove the book with the specified ID
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)