from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (can be replaced with a database)
books = {
    1: {'id': 1, 'name': 'John Doe', 'email': 'johndoe@example.com'},
    2: {'id': 2, 'name': 'Jane Smith', 'email': 'janesmith@example.com'}
}

# Get all books
@app.route('/', methods=['GET'])
def get_books():
    return render_template("index")


# Run the flask App
if __name__ == '__main__':
    app.run(debug=True)
