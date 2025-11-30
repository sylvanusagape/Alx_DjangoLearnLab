# api/urls.py

from django.urls import path
from .views import (BookListAPIView, 
    BookRetrieveAPIView, 
    BookCreateAPIView,
    BookUpdateAPIView,
    BookDeleteAPIView)

urlpatterns = [
    # 1. List View (GET)
    path('books/', 
         BookListAPIView.as_view(), 
         name='book-list'),

    # 2. Detail View (GET)
    path('books/<int:pk>/', 
         BookRetrieveAPIView.as_view(), 
         name='book-detail'),
    
    # --- New Dedicated Paths ---
    
    # 3. Create View (POST)
    path('books/create/', 
         BookCreateAPIView.as_view(), 
         name='book-create'),

    # 4. Update View (PUT/PATCH)
    path('books/update/', 
         BookUpdateAPIView.as_view(), 
         name='book-update'),
    
    # 5. Delete View (DELETE)
    path('books/delete/', 
         BookDeleteAPIView.as_view(), 
         name='book-delete'),
]