from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

urlpatterns = [
    # List all books
    path('books/', views.list_books, name='list_books'),
    # Add a new book
    path('add_book/', views.add_book, name='add_book'),
    # Edit an existing book by its primary key (book_id)
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    # Delete an existing book by its primary key (book_id)
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

    path('display/', views.display_all, name='display_all'),
    path('books/', views.list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view()), # Class-based view
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), LoginView.as_view(template_name="relationship_app/login.html")),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    path('member_view/', views.member_view, name='member_view'),
]