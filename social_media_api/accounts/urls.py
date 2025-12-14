from django.urls import path
from .views import RegisterView, LoginView, ProfileView

<<<<<<< HEAD

urlpatterns = [
path('register/', RegisterView.as_view()),
path('login/', LoginView.as_view()),
path('profile/', ProfileView.as_view()),
=======
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
>>>>>>> 7d6f437
]