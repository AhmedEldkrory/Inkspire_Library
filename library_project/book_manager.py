import os
import django
import random
import requests
import time
import base64
from datetime import datetime
from pathlib import Path
from collections import Counter
import argparse

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from django.db.models import Q, Count
from online_library.models import Category, Book

# ===== COVER IMAGE FUNCTIONS =====

def download_image(url, save_path):
    """Download an image from a URL and save it to the specified path"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def get_openlibrary_cover(title, author, isbn):
    """Try to get a book cover from Open Library API"""
    # First try by ISBN
    if isbn:
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        try:
            response = requests.get(url)
            # Check if we got a real image (not the default "no image" which is small)
            if response.status_code == 200 and len(response.content) > 1000:
                return url
        except Exception as e:
            print(f"Error fetching cover by ISBN for {title}: {e}")

    # Then try by title and author
    query = f"{title} {author}".replace(' ', '+')
    url = f"https://openlibrary.org/search.json?q={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('numFound', 0) > 0:
                # Get the first result
                first_result = data['docs'][0]

                # Check if it has a cover ID
                if 'cover_i' in first_result:
                    cover_id = first_result['cover_i']
                    return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    except Exception as e:
        print(f"Error fetching cover for {title}: {e}")

    return None

def get_google_books_cover(title, author, isbn):
    """Try to get a book cover from Google Books API"""
    # First try by ISBN
    if isbn:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('totalItems', 0) > 0:
                    item = data['items'][0]
                    if 'imageLinks' in item.get('volumeInfo', {}):
                        return item['volumeInfo']['imageLinks'].get('thumbnail')
        except Exception as e:
            print(f"Error fetching Google Books cover by ISBN for {title}: {e}")

    # Then try by title and author
    query = f"intitle:{title} inauthor:{author}".replace(' ', '+')
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('totalItems', 0) > 0:
                item = data['items'][0]
                if 'imageLinks' in item.get('volumeInfo', {}):
                    return item['volumeInfo']['imageLinks'].get('thumbnail')
    except Exception as e:
        print(f"Error fetching Google Books cover for {title}: {e}")

    return None

def generate_data_uri_placeholder(title, author):
    """Generate a simple placeholder for a book"""
    return f"/static/img/placeholder1.jpg"

def generate_placeholder_cover(book, save_path):
    """Generate a simple placeholder cover image for a book using a data URI"""
    # Create a simple SVG placeholder
    title_short = book.title[:20] + "..." if len(book.title) > 20 else book.title
    author_short = book.author[:20] + "..." if len(book.author) > 20 else book.author

    # Create a simple text file as a placeholder
    with open(save_path, 'w') as f:
        f.write(f"Title: {book.title}\n")
        f.write(f"Author: {book.author}\n")
        f.write(f"ISBN: {book.isbn}\n")

    print(f"Generated placeholder for: {book.title}")
    return True

# ===== BOOK MANAGEMENT FUNCTIONS =====

def get_categories_with_fewer_books(limit=5):
    """Get categories with fewer books"""
    categories = Category.objects.annotate(book_count=Count('books')).order_by('book_count')
    return list(categories[:limit])

def get_books_for_category(category_name, count=10):
    """Get book data for a specific category"""
    books_data = []

    # Define search queries for different categories
    category_queries = {
        'Fiction': ['fiction', 'novel', 'literature'],
        'Non-Fiction': ['non-fiction', 'biography', 'history'],
        'Science Fiction': ['science fiction', 'sci-fi', 'dystopian'],
        'Mystery': ['mystery', 'thriller', 'detective'],
        'Fantasy': ['fantasy', 'magic', 'dragons'],
        'Biography': ['biography', 'memoir', 'autobiography'],
        'History': ['history', 'historical', 'civilization'],
        'Science': ['science', 'physics', 'biology'],
        'Technology': ['technology', 'computers', 'programming'],
        'Self-Help': ['self-help', 'personal development', 'psychology']
    }

    # Get search terms for the category
    search_terms = category_queries.get(category_name, [category_name.lower()])
    search_term = random.choice(search_terms)

    # Search for books using Google Books API
    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{search_term}&maxResults=40"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('totalItems', 0) > 0:
                items = data.get('items', [])
                random.shuffle(items)  # Randomize the results

                for item in items[:count]:
                    volume_info = item.get('volumeInfo', {})

                    # Skip books without required information
                    if not all(key in volume_info for key in ['title', 'authors', 'description']):
                        continue

                    # Get ISBN if available
                    isbn = None
                    industry_identifiers = volume_info.get('industryIdentifiers', [])
                    for identifier in industry_identifiers:
                        if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                            isbn = identifier.get('identifier')
                            break

                    if not isbn:
                        # Generate a random ISBN if none is available
                        isbn = f"978{random.randint(1000000000, 9999999999)}"

                    # Get publication date if available
                    pub_date = volume_info.get('publishedDate', '2020-01-01')
                    if len(pub_date) == 4:  # Only year is provided
                        pub_date = f"{pub_date}-01-01"
                    elif len(pub_date) == 7:  # Year and month are provided
                        pub_date = f"{pub_date}-01"

                    # Create book data
                    book_data = {
                        'title': volume_info.get('title'),
                        'author': ', '.join(volume_info.get('authors', ['Unknown'])),
                        'description': volume_info.get('description', 'No description available.'),
                        'category': category_name,
                        'isbn': isbn,
                        'publication_date': pub_date,
                        'total_copies': random.randint(5, 20),
                        'available_copies': random.randint(1, 5)
                    }

                    # Check if this book already exists in our database
                    if Book.objects.filter(isbn=isbn).exists() or Book.objects.filter(title=book_data['title'], author=book_data['author']).exists():
                        continue

                    books_data.append(book_data)

                    # Break if we have enough books
                    if len(books_data) >= count:
                        break
    except Exception as e:
        print(f"Error fetching books for category {category_name}: {e}")

    return books_data

def add_books_to_category(category, books_data):
    """Add books to a category"""
    covers_dir = Path('../media/covers')
    covers_dir.mkdir(parents=True, exist_ok=True)

    added_count = 0
    for book_data in books_data:
        # Check if book already exists
        if Book.objects.filter(isbn=book_data['isbn']).exists():
            print(f"Book already exists: {book_data['title']}")
            continue

        # Convert publication_date string to date object
        try:
            publication_date = datetime.strptime(book_data['publication_date'], '%Y-%m-%d').date()
        except ValueError:
            # If date format is invalid, use current date
            publication_date = datetime.now().date()

        # Create the book
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            description=book_data['description'],
            category=category,
            isbn=book_data['isbn'],
            publication_date=publication_date,
            total_copies=book_data['total_copies'],
            available_copies=book_data['available_copies']
        )

        # Try to get a cover image
        cover_url = get_openlibrary_cover(book_data['title'], book_data['author'], book_data['isbn'])

        # If that fails, try Google Books
        if not cover_url:
            cover_url = get_google_books_cover(book_data['title'], book_data['author'], book_data['isbn'])

        if cover_url:
            # Create a filename based on the book's ISBN
            filename = f"{book_data['isbn']}.jpg"
            save_path = covers_dir / filename

            # Download the image
            if download_image(cover_url, save_path):
                # Set the book's cover_image field
                book.cover_image = f"/media/covers/{filename}"
                print(f"Downloaded cover for {book_data['title']}")
            else:
                print(f"Failed to download cover for {book_data['title']}")
        else:
            print(f"No cover found for {book_data['title']}")

        # Save the book
        book.save()
        added_count += 1
        print(f"Added book: {book.title} to category {category.name}")

        # Sleep to avoid hitting API rate limits
        time.sleep(1)

    return added_count

# ===== COMMAND FUNCTIONS =====

def add_books(count=30, predefined=False):
    """Add books to the database"""
    # Create the covers directory if it doesn't exist
    covers_dir = Path('../media/covers')
    covers_dir.mkdir(parents=True, exist_ok=True)

    # Get all categories
    categories = list(Category.objects.all())

    if predefined:
        # List of predefined books to add
        books_data = [
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'description': 'A romantic novel of manners that follows the character development of Elizabeth Bennet, who learns about the repercussions of hasty judgments.',
                'category': 'Fiction',
                'isbn': '9780141439518',
                'publication_date': '1813-01-28',
                'total_copies': 10,
                'available_copies': 8
            },
            # Add more predefined books here...
            {
                'title': 'The Odyssey',
                'author': 'Homer',
                'description': 'An ancient Greek epic poem that follows the Greek hero Odysseus on his journey home after the fall of Troy.',
                'category': 'Fiction',
                'isbn': '9780140268867',
                'publication_date': '1800-01-01',
                'total_copies': 5,
                'available_copies': 4
            },
            {
                'title': 'Brave New World',
                'author': 'Aldous Huxley',
                'description': 'A dystopian novel set in a futuristic World State, whose citizens are environmentally engineered into an intelligence-based social hierarchy.',
                'category': 'Science Fiction',
                'isbn': '9780060850524',
                'publication_date': '1932-01-01',
                'total_copies': 12,
                'available_copies': 10
            }
        ]

        # Create a dictionary to map category names to category objects
        category_dict = {category.name: category for category in categories}

        # Create books
        created_count = 0
        for book_data in books_data[:count]:
            category_name = book_data.pop('category')
            category = category_dict.get(category_name)

            if not category:
                print(f"Category '{category_name}' not found, skipping book: {book_data['title']}")
                continue

            # Check if book already exists
            if Book.objects.filter(isbn=book_data['isbn']).exists():
                print(f"Book already exists: {book_data['title']}")
                continue

            # Convert publication_date string to date object
            publication_date = datetime.strptime(book_data['publication_date'], '%Y-%m-%d').date()

            # Create the book
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                description=book_data['description'],
                category=category,
                isbn=book_data['isbn'],
                publication_date=publication_date,
                total_copies=book_data['total_copies'],
                available_copies=book_data['available_copies']
            )

            # Try to get a cover image
            cover_url = get_openlibrary_cover(book_data['title'], book_data['author'], book_data['isbn'])

            # If that fails, try Google Books
            if not cover_url:
                cover_url = get_google_books_cover(book_data['title'], book_data['author'], book_data['isbn'])

            if cover_url:
                # Create a filename based on the book's ISBN
                filename = f"{book_data['isbn']}.jpg"
                save_path = covers_dir / filename

                # Download the image
                if download_image(cover_url, save_path):
                    # Set the book's cover_image field
                    book.cover_image = f"/media/covers/{filename}"
                    print(f"Downloaded cover for {book_data['title']}")
                else:
                    print(f"Failed to download cover for {book_data['title']}")
            else:
                print(f"No cover found for {book_data['title']}")

            # Save the book
            book.save()
            created_count += 1
            print(f"Created book: {book.title}")

            # Sleep to avoid hitting API rate limits
            time.sleep(1)

        print(f"Created {created_count} new books")
    else:
        # Get categories with fewer books
        categories = get_categories_with_fewer_books(limit=5)

        # Calculate how many books to add to each category
        books_per_category = count // len(categories)

        total_added = 0
        for category in categories:
            print(f"Adding books to category: {category.name} (currently has {category.book_count} books)")

            # Get book data for this category
            books_data = get_books_for_category(category.name, count=books_per_category + 5)  # Get a few extra in case some fail

            # Add books to the category
            added = add_books_to_category(category, books_data)
            total_added += added

            print(f"Added {added} books to category {category.name}")

            # If we've added enough books, stop
            if total_added >= count:
                break

        print(f"Total books added: {total_added}")

def fix_covers():
    """Fix all book covers"""
    # Create the covers directory if it doesn't exist
    covers_dir = Path('../media/covers')
    covers_dir.mkdir(parents=True, exist_ok=True)

    # Get all books
    books = Book.objects.all()

    for book in books:
        print(f"Processing: {book.title} by {book.author}")

        # Try to get a cover from Open Library
        cover_url = get_openlibrary_cover(book.title, book.author, book.isbn)

        # If that fails, try Google Books
        if not cover_url:
            cover_url = get_google_books_cover(book.title, book.author, book.isbn)

        if cover_url:
            # Create a filename based on the book's ISBN
            filename = f"{book.isbn}.jpg"
            save_path = covers_dir / filename

            # Download the image
            if download_image(cover_url, save_path):
                # Update the book's cover_image field
                book.cover_image = f"/media/covers/{filename}"
                book.save()
                print(f"Downloaded cover for {book.title}")
            else:
                # If download fails, use a placeholder
                book.cover_image = "/static/img/placeholder1.jpg"
                book.save()
                print(f"Using placeholder for {book.title}")
        else:
            # If no cover found, use a placeholder
            book.cover_image = "/static/img/placeholder1.jpg"
            book.save()
            print(f"Using placeholder for {book.title}")

        # Sleep to avoid hitting API rate limits
        time.sleep(1)

def fix_missing_covers():
    """Fix books with missing covers"""
    # Get all books without covers
    books_without_covers = Book.objects.filter(
        Q(cover_image__isnull=True) |
        Q(cover_image='')
    )

    count = 0
    for book in books_without_covers:
        # Use a static placeholder
        book.cover_image = "/static/img/placeholder1.jpg"
        book.save()
        count += 1
        print(f"Fixed cover for: {book.title}")

    print(f"Fixed {count} books with missing covers")

def generate_placeholders():
    """Generate placeholder covers for books without covers"""
    # Get all books without covers
    books_without_covers = Book.objects.filter(
        Q(cover_image__isnull=True) |
        Q(cover_image='') |
        Q(cover_image__startswith='/media/covers/placeholder')
    )

    count = 0
    for book in books_without_covers:
        # Use a static placeholder
        book.cover_image = "/static/img/placeholder1.jpg"
        book.save()
        count += 1
        print(f"Added placeholder for: {book.title}")

    # Also check for books with covers that don't exist on disk
    all_books = Book.objects.exclude(
        Q(cover_image__isnull=True) |
        Q(cover_image='')
    )

    covers_dir = Path('../media/covers')
    for book in all_books:
        if book.cover_image and not book.cover_image.startswith('/static/img/'):
            # Extract the filename from the cover_image path
            filename = os.path.basename(book.cover_image)
            file_path = covers_dir / filename

            # Check if the file exists
            if not file_path.exists():
                # Use a static placeholder
                book.cover_image = "/static/img/placeholder1.jpg"
                book.save()
                count += 1
                print(f"Added placeholder for: {book.title}")

    print(f"Generated {count} placeholder covers")

def download_all_covers():
    """Download covers for all books"""
    # Create the covers directory if it doesn't exist
    covers_dir = Path('../media/covers')
    covers_dir.mkdir(parents=True, exist_ok=True)

    # Get all books
    books = Book.objects.all()

    for book in books:
        # Skip books that already have a cover image
        if book.cover_image and not book.cover_image.startswith('/media/covers/placeholder'):
            print(f"Skipping {book.title} - already has a cover")
            continue

        print(f"Finding cover for: {book.title} by {book.author}")

        # Get the cover URL
        cover_url = get_openlibrary_cover(book.title, book.author, book.isbn)

        # If that fails, try Google Books
        if not cover_url:
            cover_url = get_google_books_cover(book.title, book.author, book.isbn)

        if cover_url:
            # Create a filename based on the book's ISBN
            filename = f"{book.isbn}.jpg"
            save_path = covers_dir / filename

            # Download the image
            if download_image(cover_url, save_path):
                # Update the book's cover_image field
                book.cover_image = f"/media/covers/{filename}"
                book.save()
                print(f"Downloaded cover for {book.title}")
            else:
                print(f"Failed to download cover for {book.title}")
        else:
            print(f"No cover found for {book.title}")

        # Sleep to avoid hitting API rate limits
        time.sleep(1)

# ===== MAIN FUNCTION =====

def main():
    parser = argparse.ArgumentParser(description='Book Manager - A tool for managing books in the library')

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Add books command
    add_parser = subparsers.add_parser('add', help='Add books to the database')
    add_parser.add_argument('--count', type=int, default=30, help='Number of books to add')
    add_parser.add_argument('--predefined', action='store_true', help='Use predefined book data')

    # Fix covers command
    subparsers.add_parser('fix-covers', help='Fix all book covers')

    # Fix missing covers command
    subparsers.add_parser('fix-missing', help='Fix books with missing covers')

    # Generate placeholders command
    subparsers.add_parser('generate-placeholders', help='Generate placeholder covers for books without covers')

    # Download all covers command
    subparsers.add_parser('download-covers', help='Download covers for all books')

    # Parse arguments
    args = parser.parse_args()

    # Run the appropriate command
    if args.command == 'add':
        add_books(args.count, args.predefined)
    elif args.command == 'fix-covers':
        fix_covers()
    elif args.command == 'fix-missing':
        fix_missing_covers()
    elif args.command == 'generate-placeholders':
        generate_placeholders()
    elif args.command == 'download-covers':
        download_all_covers()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
