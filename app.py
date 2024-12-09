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
            for book in books:
                if book["id"] == book_id:
                    # Update only the provided fields, keeping the rest intact
                    book["title"] = request.form.get("title") or book["title"]
                    book["author"] = request.form.get(
                        "author") or book["author"]
                    break

        elif action == "delete":
            book_id = int(request.form.get("book_id"))
            books[:] = [book for book in books if book["id"] != book_id]

        return redirect(url_for("home"))

    return render_template("index.html", books=books)


if __name__ == "__main__":
    app.run(debug=True)
