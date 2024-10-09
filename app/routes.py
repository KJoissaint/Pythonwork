from flask import Blueprint, jsonify, request, abort
from .models import load_books, save_books, find_book_by_id
import os

bp = Blueprint('api', __name__)

csv_file = os.path.join(os.path.dirname(__file__), '../data/books.csv')

@bp.route('/books', methods=['GET'])
def get_books():
    books = load_books(csv_file)
    return jsonify([book.__dict__ for book in books])

@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book_by_id(book_id, csv_file)
    if book:
        return jsonify(book.__dict__)
    else:
        abort(404, description="Book not found")


@bp.route('/books', methods=['POST'])
def create_book():
    new_book_data = request.json
    new_book = Book(
        title=new_book_data.get('title'),
        author=new_book_data.get('author'),
        publication_date=new_book_data.get('publication_date'),
        genre=new_book_data.get('genre')
    )
    
    books = load_books(csv_file)
    books.append(new_book)
    save_books(csv_file, books)
    
    return jsonify(new_book.__dict__), 201

@bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_data = request.json
    books = load_books(csv_file)
    
    for book in books:
        if book.id == book_id:
            book.title = updated_data.get('title', book.title)
            book.author = updated_data.get('author', book.author)
            book.publication_date = updated_data.get('publication_date', book.publication_date)
            book.genre = updated_data.get('genre', book.genre)
            save_books(csv_file, books)
            return jsonify(book.__dict__)
    
    abort(404, description="Book not found")

@bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = load_books(csv_file)
    books = [book for book in books if book.id != book_id]
    
    if len(books) < len(load_books(csv_file)):  # Si un livre a été supprimé
        save_books(csv_file, books)
        return jsonify({"message": "Book deleted"}), 200
    else:
        abort(404, description="Book not found")
