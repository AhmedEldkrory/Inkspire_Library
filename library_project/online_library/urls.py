from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Book-related URLs
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/<int:book_id>/buy/', views.buy_book, name='buy_book'),
    path('books/<int:book_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),

    # User-related URLs
    path('my-borrowings/', views.my_borrowings, name='my_borrowings'),
    path('my-borrowings/<int:borrow_id>/return/', views.return_book, name='return_book'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),

    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/books/', views.manage_books, name='manage_books'),
    path('admin/books/add/', views.add_book, name='add_book'),
    path('admin/books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('admin/books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('admin/borrow-requests/', views.manage_borrow_requests, name='manage_borrow_requests'),
    path('admin/borrow-requests/<int:request_id>/update/', views.update_borrow_request, name='update_borrow_request'),

    # Search URL
    path('search/', views.search_books, name='search_books'),

    # About and Contact URLs
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
]