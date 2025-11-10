from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    path('display/', views.display_all, name='display_all'),
    path('books/', views.list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), name='library_detail')
]