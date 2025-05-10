import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from online_library.models import Category, Book, User, Review
from django.utils import timezone

def create_categories():
    """Create book categories"""
    categories = [
        {
            'name': 'Fiction',
            'description': 'Novels, short stories, and other fictional works'
        },
        {
            'name': 'Non-Fiction',
            'description': 'Factual works, biographies, and informational texts'
        },
        {
            'name': 'Science Fiction',
            'description': 'Speculative fiction dealing with imaginative concepts'
        },
        {
            'name': 'Mystery',
            'description': 'Fiction dealing with the solution of a crime or puzzle'
        },
        {
            'name': 'Fantasy',
            'description': 'Fiction featuring magical and supernatural elements'
        },
        {
            'name': 'Biography',
            'description': 'Detailed descriptions of a person\'s life'
        },
        {
            'name': 'History',
            'description': 'Books about historical events and periods'
        },
        {
            'name': 'Science',
            'description': 'Books about scientific discoveries and concepts'
        },
        {
            'name': 'Technology',
            'description': 'Books about technological advancements and computing'
        },
        {
            'name': 'Self-Help',
            'description': 'Books aimed at personal improvement'
        }
    ]
    
    created_categories = []
    for category_data in categories:
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            defaults={'description': category_data['description']}
        )
        created_categories.append(category)
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
    
    return created_categories

def create_books(categories):
    """Create sample books"""
    books_data = [
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'description': 'The story of young Scout Finch and her father Atticus, a lawyer who defends a black man accused of raping a white woman in the 1930s Alabama.',
            'category': 'Fiction',
            'isbn': '9780061120084',
            'publication_date': '1960-07-11',
            'total_copies': 10,
            'available_copies': 8,
            'cover_image': '/media/covers/to_kill_a_mockingbird.jpg'
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'description': 'A dystopian novel set in a totalitarian society where critical thought is suppressed under a regime of surveillance and propaganda.',
            'category': 'Fiction',
            'isbn': '9780451524935',
            'publication_date': '1949-06-08',
            'total_copies': 15,
            'available_copies': 12,
            'cover_image': '/media/covers/1984.jpg'
        },
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'description': 'The story of eccentric millionaire Jay Gatsby and his pursuit of Daisy Buchanan, exploring themes of decadence and idealism.',
            'category': 'Fiction',
            'isbn': '9780743273565',
            'publication_date': '1925-04-10',
            'total_copies': 8,
            'available_copies': 5,
            'cover_image': '/media/covers/great_gatsby.jpg'
        },
        {
            'title': 'A Brief History of Time',
            'author': 'Stephen Hawking',
            'description': 'A landmark volume in science writing that explains complex concepts of cosmology in an accessible way.',
            'category': 'Science',
            'isbn': '9780553380163',
            'publication_date': '1988-09-01',
            'total_copies': 7,
            'available_copies': 6,
            'cover_image': '/media/covers/brief_history_time.jpg'
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'description': 'The adventure of Bilbo Baggins, a hobbit who embarks on an unexpected journey to reclaim the Lonely Mountain from the dragon Smaug.',
            'category': 'Fantasy',
            'isbn': '9780547928227',
            'publication_date': '1937-09-21',
            'total_copies': 20,
            'available_copies': 15,
            'cover_image': '/media/covers/hobbit.jpg'
        },
        {
            'title': 'Sapiens: A Brief History of Humankind',
            'author': 'Yuval Noah Harari',
            'description': 'A survey of the history of humankind from the evolution of archaic human species to the 21st century.',
            'category': 'History',
            'isbn': '9780062316097',
            'publication_date': '2014-02-10',
            'total_copies': 12,
            'available_copies': 10,
            'cover_image': '/media/covers/sapiens.jpg'
        },
        {
            'title': 'The Alchemist',
            'author': 'Paulo Coelho',
            'description': 'A philosophical novel about a young Andalusian shepherd who dreams of finding a worldly treasure and embarks on a journey to find it.',
            'category': 'Fiction',
            'isbn': '9780061122415',
            'publication_date': '1988-01-01',
            'total_copies': 15,
            'available_copies': 12,
            'cover_image': '/media/covers/alchemist.jpg'
        },
        {
            'title': 'The Da Vinci Code',
            'author': 'Dan Brown',
            'description': 'A mystery thriller novel that follows symbologist Robert Langdon as he investigates a murder in the Louvre Museum.',
            'category': 'Mystery',
            'isbn': '9780307474278',
            'publication_date': '2003-03-18',
            'total_copies': 18,
            'available_copies': 14,
            'cover_image': '/media/covers/da_vinci_code.jpg'
        },
        {
            'title': 'Dune',
            'author': 'Frank Herbert',
            'description': 'A science fiction novel set in the distant future amidst a feudal interstellar society where noble houses control planetary fiefs.',
            'category': 'Science Fiction',
            'isbn': '9780441172719',
            'publication_date': '1965-08-01',
            'total_copies': 10,
            'available_copies': 8,
            'cover_image': '/media/covers/dune.jpg'
        },
        {
            'title': 'Steve Jobs',
            'author': 'Walter Isaacson',
            'description': 'The biography of Apple co-founder Steve Jobs, based on more than forty interviews with Jobs over two years.',
            'category': 'Biography',
            'isbn': '9781451648539',
            'publication_date': '2011-10-24',
            'total_copies': 8,
            'available_copies': 7,
            'cover_image': '/media/covers/steve_jobs.jpg'
        },
        {
            'title': 'Thinking, Fast and Slow',
            'author': 'Daniel Kahneman',
            'description': 'A book that summarizes research that Kahneman conducted over decades, often in collaboration with Amos Tversky, on cognitive biases and happiness.',
            'category': 'Non-Fiction',
            'isbn': '9780374533557',
            'publication_date': '2011-10-25',
            'total_copies': 9,
            'available_copies': 7,
            'cover_image': '/media/covers/thinking_fast_slow.jpg'
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'description': 'A novel about a teenager named Holden Caulfield who experiences disillusionment and alienation after being expelled from prep school.',
            'category': 'Fiction',
            'isbn': '9780316769488',
            'publication_date': '1951-07-16',
            'total_copies': 12,
            'available_copies': 9,
            'cover_image': '/media/covers/catcher_rye.jpg'
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'description': 'An epic high-fantasy novel that follows hobbits Frodo and Sam as they journey to destroy the One Ring and defeat the Dark Lord Sauron.',
            'category': 'Fantasy',
            'isbn': '9780618640157',
            'publication_date': '1954-07-29',
            'total_copies': 25,
            'available_copies': 20,
            'cover_image': '/media/covers/lord_rings.jpg'
        },
        {
            'title': 'The Immortal Life of Henrietta Lacks',
            'author': 'Rebecca Skloot',
            'description': 'A non-fiction book about Henrietta Lacks, whose cancer cells were the source of the HeLa cell line, important in medical research.',
            'category': 'Science',
            'isbn': '9781400052189',
            'publication_date': '2010-02-02',
            'total_copies': 7,
            'available_copies': 6,
            'cover_image': '/media/covers/henrietta_lacks.jpg'
        },
        {
            'title': 'The Girl with the Dragon Tattoo',
            'author': 'Stieg Larsson',
            'description': 'A psychological thriller that follows journalist Mikael Blomkvist and hacker Lisbeth Salander as they investigate a wealthy family.',
            'category': 'Mystery',
            'isbn': '9780307454546',
            'publication_date': '2005-08-01',
            'total_copies': 14,
            'available_copies': 10,
            'cover_image': '/media/covers/dragon_tattoo.jpg'
        },
        {
            'title': 'Educated',
            'author': 'Tara Westover',
            'description': 'A memoir about a woman who was raised in a survivalist family in Idaho and her journey to education.',
            'category': 'Biography',
            'isbn': '9780399590504',
            'publication_date': '2018-02-20',
            'total_copies': 10,
            'available_copies': 8,
            'cover_image': '/media/covers/educated.jpg'
        },
        {
            'title': 'The Martian',
            'author': 'Andy Weir',
            'description': 'A science fiction novel about an astronaut who becomes stranded alone on Mars and must improvise to survive.',
            'category': 'Science Fiction',
            'isbn': '9780553418026',
            'publication_date': '2014-02-11',
            'total_copies': 15,
            'available_copies': 12,
            'cover_image': '/media/covers/martian.jpg'
        },
        {
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'description': 'A practical guide to breaking bad habits and building good ones, based on scientific research.',
            'category': 'Self-Help',
            'isbn': '9780735211292',
            'publication_date': '2018-10-16',
            'total_copies': 20,
            'available_copies': 15,
            'cover_image': '/media/covers/atomic_habits.jpg'
        },
        {
            'title': 'The Silent Patient',
            'author': 'Alex Michaelides',
            'description': 'A psychological thriller about a woman who shoots her husband and then stops speaking, and the therapist determined to get her to talk.',
            'category': 'Mystery',
            'isbn': '9781250301697',
            'publication_date': '2019-02-05',
            'total_copies': 12,
            'available_copies': 9,
            'cover_image': '/media/covers/silent_patient.jpg'
        },
        {
            'title': 'The Power of Habit',
            'author': 'Charles Duhigg',
            'description': 'An examination of the science behind habit creation and reformation, explaining how habits work and how they can be changed.',
            'category': 'Self-Help',
            'isbn': '9780812981605',
            'publication_date': '2012-02-28',
            'total_copies': 10,
            'available_copies': 8,
            'cover_image': '/media/covers/power_habit.jpg'
        }
    ]
    
    created_books = []
    category_dict = {category.name: category for category in categories}
    
    for book_data in books_data:
        category_name = book_data.pop('category')
        category = category_dict.get(category_name)
        
        if not category:
            print(f"Category '{category_name}' not found, skipping book: {book_data['title']}")
            continue
        
        # Convert publication_date string to date object
        publication_date = datetime.strptime(book_data['publication_date'], '%Y-%m-%d').date()
        book_data['publication_date'] = publication_date
        
        # Add category to book data
        book_data['category'] = category
        
        # Check if book already exists
        existing_book = Book.objects.filter(isbn=book_data['isbn']).first()
        if existing_book:
            print(f"Book already exists: {book_data['title']}")
            created_books.append(existing_book)
            continue
        
        # Create new book
        book = Book.objects.create(**book_data)
        created_books.append(book)
        print(f"Created book: {book.title}")
    
    return created_books

def create_reviews(books):
    """Create sample reviews for books"""
    # Make sure we have at least one user
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # Create some regular users if they don't exist
    users = [admin_user]
    for i in range(1, 6):
        user, created = User.objects.get_or_create(
            username=f'user{i}',
            defaults={
                'email': f'user{i}@example.com',
                'role': 'user',
                'first_name': f'User {i}',
                'last_name': 'Test'
            }
        )
        if created:
            user.set_password(f'password{i}')
            user.save()
            print(f"Created user: {user.username}")
        users.append(user)
    
    # Sample comments for reviews
    positive_comments = [
        "Absolutely loved this book! Couldn't put it down.",
        "One of the best books I've read this year.",
        "The characters were so well developed and the plot was engaging.",
        "A masterpiece that will stand the test of time.",
        "Beautifully written with a compelling narrative.",
        "I was completely immersed in the story from start to finish.",
        "The author's writing style is exceptional.",
        "A thought-provoking read that stayed with me long after I finished it.",
        "Highly recommend this to anyone who enjoys this genre.",
        "The perfect balance of plot, character development, and pacing."
    ]
    
    mixed_comments = [
        "Good book overall, but some parts dragged a bit.",
        "Interesting premise but the execution could have been better.",
        "Liked the characters but found the plot somewhat predictable.",
        "Worth reading, though not as amazing as I expected.",
        "Some brilliant moments, but also some sections that didn't work for me.",
        "A solid read, but not something I'd read again.",
        "The first half was excellent, but it lost momentum towards the end.",
        "Good but not great. Had potential to be more impactful.",
        "Enjoyed it, but it didn't quite live up to the hype.",
        "Decent story with some memorable scenes, but also some flaws."
    ]
    
    critical_comments = [
        "Had trouble connecting with the characters.",
        "The plot had too many holes to be believable.",
        "Found the writing style difficult to engage with.",
        "Struggled to finish this one.",
        "The pacing was off, making it hard to stay interested.",
        "Disappointing compared to the author's other works.",
        "The premise was promising but the execution fell flat.",
        "Too many clichés and predictable twists.",
        "Didn't live up to my expectations at all.",
        "The characters felt one-dimensional and underdeveloped."
    ]
    
    # Create reviews
    review_count = 0
    for book in books:
        # Determine how many reviews to create for this book (1-5)
        num_reviews = random.randint(1, 5)
        
        # Select random users to write reviews
        book_reviewers = random.sample(users, min(num_reviews, len(users)))
        
        for user in book_reviewers:
            # Check if user already reviewed this book
            if Review.objects.filter(user=user, book=book).exists():
                continue
            
            # Determine rating (1-5)
            rating = random.randint(1, 5)
            
            # Select appropriate comment based on rating
            if rating >= 4:
                comment = random.choice(positive_comments)
            elif rating == 3:
                comment = random.choice(mixed_comments)
            else:
                comment = random.choice(critical_comments)
            
            # Create review
            Review.objects.create(
                user=user,
                book=book,
                rating=rating,
                comment=comment
            )
            review_count += 1
            
    print(f"Created {review_count} reviews")

def main():
    print("Starting data population...")
    
    # Create categories
    categories = create_categories()
    
    # Create books
    books = create_books(categories)
    
    # Create reviews
    create_reviews(books)
    
    print("Data population complete!")

if __name__ == "__main__":
    main()
