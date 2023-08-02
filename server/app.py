from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # Import the Bcrypt module for password hashing
from models import User, Book, Review, Order
from config import db, app

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

@app.route('/api/register', methods=['POST'])
def register_user():
    # Get the data from the request body
    data = request.get_json()

    # Extract user data from the request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if any of the required fields are missing
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required.'}), 400

    # Check if the user already exists with the same username or email
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already taken. Please choose a different username.'}), 400

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({'error': 'Email address already registered. Please use a different email.'}), 400

    # Create a new user object
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201

# Route to log in an existing user
@app.route('/api/login', methods=['POST'])
def login_user():
    # Get the data from the request body
    data = request.get_json()

    # Extract user data from the request
    username = data.get('username')
    password = data.get('password')

    # Check if any of the required fields are missing
    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    # Find the user with the provided username in the database
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and if the password is correct
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password.'}), 401

    # If the user exists and the password is correct, return a success message
    return jsonify({'message': 'Login successful.'}), 200
# Route to get a list of all books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    # Fetch all books from the database
    books = Book.query.all()

    # Serialize the books data
    serialized_books = [book.serialize() for book in books]

    # Return the serialized books as a JSON response
    return jsonify(serialized_books)

# Route to get book details by ID
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    # Fetch the book from the database by ID
    book = Book.query.get(id)

    if book is None:
        # If book with given ID doesn't exist, return a 404 response
        return jsonify({'error': 'Book not found'}), 404

    # Serialize the book data
    serialized_book = book.serialize()

    # Return the serialized book as a JSON response
    return jsonify(serialized_book)
# Route to get all reviews for a book by ID
@app.route('/api/books/<int:id>/reviews', methods=['GET'])
def get_reviews_by_book_id(id):
    # Fetch the book from the database by ID
    book = Book.query.get(id)

    if book is None:
        # If book with given ID doesn't exist, return a 404 response
        return jsonify({'error': 'Book not found'}), 404

    # Fetch all reviews for the book
    reviews = Review.query.filter_by(book_id=id).all()

    # Serialize the reviews data
    serialized_reviews = [review.serialize() for review in reviews]

    # Return the serialized reviews as a JSON response
    return jsonify(serialized_reviews)

# Route to add a new review for a book
@app.route('/api/books/<int:id>/reviews', methods=['POST'])
def add_review_for_book(id):
    # Fetch the book from the database by ID
    book = Book.query.get(id)

    if book is None:
        # If book with given ID doesn't exist, return a 404 response
        return jsonify({'error': 'Book not found'}), 404

    # Get the data from the request
    data = request.json

    # Extract review details from the data
    text = data.get('text')
    rating = data.get('rating')

    # Create a new review object
    review = Review(text=text, rating=rating, book=book)

    # Add the review to the database
    db.session.add(review)
    db.session.commit()

    # Return the serialized review as a JSON response
    return jsonify(review.serialize()), 201

# Route to update a review by ID
@app.route('/api/reviews/<int:id>', methods=['PUT'])
def update_review_by_id(id):
    # Fetch the review from the database by ID
    review = Review.query.get(id)

    if review is None:
        # If review with given ID doesn't exist, return a 404 response
        return jsonify({'error': 'Review not found'}), 404

    # Get the data from the request
    data = request.json

    # Update review details from the data
    review.text = data.get('text', review.text)
    review.rating = data.get('rating', review.rating)

    # Commit the changes to the database
    db.session.commit()

    # Return the serialized review as a JSON response
    return jsonify(review.serialize())

# Route to delete a review by ID
@app.route('/api/reviews/<int:id>', methods=['DELETE'])
def delete_review_by_id(id):
    # Fetch the review from the database by ID
    review = Review.query.get(id)

    if review is None:
        # If review with given ID doesn't exist, return a 404 response
        return jsonify({'error': 'Review not found'}), 404

    # Delete the review from the database
    db.session.delete(review)
    db.session.commit()

    # Return a success message as a JSON response
    return jsonify({'message': 'Review deleted successfully'}), 200
# Route to place a new order
@app.route('/api/orders', methods=['POST'])
def place_new_order():
    # Get the data from the request
    data = request.json

    # Extract order details from the data
    status = data.get('status', 'pending')
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    # Fetch the user from the database by ID
    user = User.query.get(user_id)

    if user is None:
        # If user with given ID doesn't exist, return a 404 response
        return jsonify({'error': 'User not found'}), 404

    # Fetch the book from the database by ID
    book = Book.query.get(book_id)

    if book is None:
        # If book with given ID doesn't exist, return a 404 response
        return jsonify({'error': 'Book not found'}), 404

    # Create a new order object
    order = Order(status=status, user=user, book=book)

    # Add the order to the database
    db.session.add(order)
    db.session.commit()

    # Return the serialized order as a JSON response
    return jsonify(order.serialize()), 201

# Route to get order details by ID
@app.route('/api/orders/<int:id>', methods=['GET'])
def get_order_by_id(id):
    # Fetch the order from the database by ID
    order = Order.query.get(id)

    if order is None:
        # If order with given ID doesn't exist, return a 404 response
        return jsonify({'error': 'Order not found'}), 404

    # Return the serialized order as a JSON response
    return jsonify(order.serialize())

if __name__ == '__main__':
    app.run(port=5555, debug=True)
