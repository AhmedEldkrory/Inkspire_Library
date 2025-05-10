from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Book, Review, BorrowRequest, Category

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'address']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'category', 'cover_image', 'pdf_file', 
                 'isbn', 'publication_date', 'total_copies']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['return_date']
        widgets = {
            'return_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    author = forms.CharField(max_length=100, required=False) 