from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data (can be replaced with a database)
books = [
    {'id': 1, 'title': 'Book One', 'author': 'John Doe'},
    {'id': 2, 'title': 'Book Two', 'author': 'Jane Smith'}
]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "create":
            title = request.form.get("title")
            author = request.form.get("author")
            if title and author:
                books.append(
                    {'id': len(books) + 1, 'title': title, 'author': author})

        elif action == "update":
            book_id = int(request.form.get("book_id"))
            title = request.form.get("title")
            author = request.form.get("author")
            for book in books:
                if book["id"] == book_id:
                    book["title"] = title
                    book["author"] = author
                    break

        elif action == "delete":
            book_id = int(request.form.get("book_id"))
            global books
            books = [book for book in books if book["id"] != book_id]

        return redirect(url_for("home"))

    return render_template("index.html", books=books)


if __name__ == "__main__":
    app.run(debug=True)
