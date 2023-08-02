from config import db, app
import bcrypt
from datetime import datetime
from models import User, Book, Review, Order

def populate_database():
    # Create users
    user1 = User(username='john_doe', email='john@example.com', role='admin')
    user1.set_password('password123')

    user2 = User(username='jane_smith', email='jane@example.com')
    user2.set_password('password456')

    # Create books
    book1 = Book(title='Sample Book 1', author='John Author', genre='Fiction', isbn='1234567890')
    book2 = Book(title='Sample Book 2', author='Jane Writer', genre='Non-Fiction', isbn='0987654321')

    # Commit users and books to the database
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(book1)
    db.session.add(book2)
    db.session.commit()

    # Create reviews and orders
    review1 = Review(text='Great book!', rating=4.5, user_id=user1.id, book_id=book1.id)
    review2 = Review(text='Interesting read.', rating=3.8, user_id=user2.id, book_id=book2.id)

    order1 = Order(status='completed', user_id=user1.id, book_id=book1.id)
    order2 = Order(status='pending', user_id=user2.id, book_id=book2.id)

    # Commit reviews and orders to the database
    db.session.add(review1)
    db.session.add(review2)
    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()

    print("Database populated successfully!")

if __name__ == '__main__':
    with app.app_context():
        populate_database()
