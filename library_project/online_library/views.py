from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import User, Book, Category, BorrowRequest, Review, Favorite, Notification
from .forms import (UserRegistrationForm, UserLoginForm, BookForm, ReviewForm,
                   BorrowRequestForm, CategoryForm, SearchForm)

def is_admin(user):
    return user.role == 'admin'

def home(request):
    categories = Category.objects.all().order_by('name')
    featured_books = Book.objects.filter(available_copies__gt=0).order_by('-created_at')[:6]
    search_form = SearchForm()

    context = {
        'categories': categories,
        'featured_books': featured_books,
        'search_form': search_form,
    }
    return render(request, 'online_library/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'online_library/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'online_library/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def book_list(request):
    books = Book.objects.filter(available_copies__gt=0)
    search_form = SearchForm(request.GET)

    # Get sort parameter from request
    sort = request.GET.get('sort', 'title')

    # Apply sorting based on parameter
    if sort == 'title':
        books = books.order_by('title')
    elif sort == 'author':
        books = books.order_by('author')
    elif sort == 'rating':
        books = books.order_by('-average_rating')
    elif sort == 'newest':
        books = books.order_by('-publication_date')
    else:
        # Default ordering by title
        books = books.order_by('title')

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        author = search_form.cleaned_data.get('author')

        if query:
            books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
        if category:
            books = books.filter(category=category)
        if author:
            books = books.filter(author__icontains=author)

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,
        'search_form': search_form,
    }
    return render(request, 'online_library/book_list.html', context)

def book_detail(request, book_id):
    # Print debug information
    print(f"Requested book ID: {book_id}")

    # Force book_id to be an integer to avoid any type issues
    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        # If conversion fails, use a default ID or redirect
        print(f"Invalid book ID: {book_id}, redirecting to book list")
        return redirect('book_list')

    book = get_object_or_404(Book, id=book_id)
    print(f"Found book: {book.title} (ID: {book.id})")

    reviews = Review.objects.filter(book=book)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()

    # Get related books (same category, excluding current book)
    related_books = Book.objects.filter(category=book.category).exclude(id=book.id).order_by('title')[:6]

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('book_detail', book_id=book_id)
    else:
        review_form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'is_favorite': is_favorite,
        'related_books': related_books,
    }
    return render(request, 'online_library/book_detail.html', context)

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BorrowRequestForm(request.POST)
        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.user = request.user
            borrow_request.book = book
            borrow_request.borrow_date = timezone.now()
            borrow_request.save()

            book.available_copies -= 1
            book.save()

            messages.success(request, 'Borrow request submitted successfully!')
            return redirect('my_borrowings')
    else:
        form = BorrowRequestForm()

    context = {
        'book': book,
        'form': form,
    }
    return render(request, 'online_library/borrow_book.html', context)

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # Process the purchase
        messages.success(request, f'You have successfully purchased "{book.title}" for ${book.buy_price}!')
        return redirect('book_detail', book_id=book.id)

    context = {
        'book': book,
    }
    return render(request, 'online_library/buy_book.html', context)

@login_required
def my_borrowings(request):
    borrowings = BorrowRequest.objects.filter(user=request.user).order_by('-request_date')
    context = {
        'borrowings': borrowings,
    }
    return render(request, 'online_library/my_borrowings.html', context)

@login_required
def return_book(request, borrow_id):
    borrow_request = get_object_or_404(BorrowRequest, id=borrow_id, user=request.user)

    if borrow_request.status == 'approved' and not borrow_request.actual_return_date:
        borrow_request.status = 'returned'
        borrow_request.actual_return_date = timezone.now()
        borrow_request.save()

        # Increase available copies
        book = borrow_request.book
        book.available_copies += 1
        book.save()

        messages.success(request, f'You have successfully returned "{book.title}".')

    return redirect('my_borrowings')

@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {
        'favorites': favorites,
    }
    return render(request, 'online_library/my_favorites.html', context)

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    context = {
        'reviews': reviews,
    }
    return render(request, 'online_library/my_reviews.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    pending_requests = BorrowRequest.objects.filter(status='pending')
    total_books = Book.objects.count()
    total_users = User.objects.count()
    total_borrowings = BorrowRequest.objects.count()

    context = {
        'pending_requests': pending_requests,
        'total_books': total_books,
        'total_users': total_users,
        'total_borrowings': total_borrowings,
    }
    return render(request, 'online_library/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_books(request):
    books = Book.objects.all().order_by('title')
    context = {
        'books': books,
    }
    return render(request, 'online_library/manage_books.html', context)

@login_required
@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('manage_books')
    else:
        form = BookForm()

    context = {
        'form': form,
    }
    return render(request, 'online_library/add_book.html', context)

@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('manage_books')
    else:
        form = BookForm(instance=book)

    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'online_library/edit_book.html', context)

@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('manage_books')

@login_required
@user_passes_test(is_admin)
def manage_borrow_requests(request):
    requests = BorrowRequest.objects.all().order_by('-request_date')
    context = {
        'requests': requests,
    }
    return render(request, 'online_library/manage_borrow_requests.html', context)

@login_required
@user_passes_test(is_admin)
def update_borrow_request(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        borrow_request.status = status

        if status == 'approved':
            borrow_request.borrow_date = timezone.now()
            borrow_request.return_date = timezone.now() + timedelta(days=14)
        elif status == 'returned':
            borrow_request.actual_return_date = timezone.now()
            borrow_request.book.available_copies += 1
            borrow_request.book.save()

        borrow_request.save()
        messages.success(request, 'Borrow request updated successfully!')
        return redirect('manage_borrow_requests')

    context = {
        'borrow_request': borrow_request,
    }
    return render(request, 'online_library/update_borrow_request.html', context)

def search_books(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )[:5]

        results = []
        for book in books:
            cover_url = None
            if book.cover_image:
                # Check if cover_image is a string (URL) or a FileField
                if isinstance(book.cover_image, str):
                    cover_url = book.cover_image
                else:
                    try:
                        cover_url = book.cover_image.url
                    except:
                        cover_url = None

            results.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'cover_url': cover_url,
            })

        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'online_library/category_list.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category).order_by('title')

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'books': page_obj,
    }
    return render(request, 'online_library/category_detail.html', context)

def about(request):
    """View for the About Library page"""
    context = {
        'library_name': 'Inkspire',
        'location': 'Hogwarts Castle',
        'established': '2025',
        'collection_size': '10,000+ books',
        'mission': 'To provide magical knowledge and literary adventures to all wizards, witches, and muggles alike.',
        'vision': 'To be the premier magical library that bridges the gap between magical and non-magical literature, fostering understanding and growth across all communities.'
    }
    return render(request, 'online_library/about.html', context)

def contact(request):
    """View for the Contact Us page"""
    context = {
        'address': 'Hogwarts Castle',
        'phone': '+201024030511',
        'email': 'ahmed.a.eldkrory@gmail.com',
        'hours': {
            'Monday-Friday': '9:00 AM - 8:00 PM',
            'Saturday': '10:00 AM - 6:00 PM',
            'Sunday': '12:00 PM - 5:00 PM'
        }
    }
    return render(request, 'online_library/contact.html', context)