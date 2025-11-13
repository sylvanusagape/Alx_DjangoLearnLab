from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views
from .views import list_books

urlpatterns = [
    path('display/', views.display_all, name='display_all'),
    path('books/', views.list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view()), # Class-based view
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), LoginView.as_view(template_name="relationship_app/login.html"))
]