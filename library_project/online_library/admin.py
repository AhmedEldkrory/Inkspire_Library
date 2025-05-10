from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Category, BorrowRequest, Review, Favorite, Notification

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'available_copies', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'author', 'isbn')
    date_hierarchy = 'created_at'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'request_date', 'return_date')
    list_filter = ('status', 'request_date')
    search_fields = ('user__username', 'book__title')
    date_hierarchy = 'request_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'book__title')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    search_fields = ('user__username', 'book__title')
    date_hierarchy = 'created_at'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    date_hierarchy = 'created_at' 