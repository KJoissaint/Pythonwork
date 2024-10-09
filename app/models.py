import csv

class Book:
    _id_counter = 1

    def __init__(self, title, author, publication_date, genre, book_id=None):
        self.id = book_id if book_id else Book._id_counter
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.genre = genre
        Book._id_counter += 1

def load_books(csv_file):
    books = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            book = Book(
                row['Titre'], row['Auteur'], row['Date de publication'], row['Genre'], book_id=int(row['ID'])
            )
            books.append(book)
    return books

def save_books(csv_file, books):
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['ID', 'Titre', 'Auteur', 'Date de publication', 'Genre']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow({
                'ID': book.id,
                'Titre': book.title,
                'Auteur': book.author,
                'Date de publication': book.publication_date,
                'Genre': book.genre
            })

def find_book_by_id(book_id, csv_file):
    books = load_books(csv_file)
    for book in books:
        if book.id == book_id:
            return book
    return None
