from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from .query_samples import insert_sample_data, get_all_books, get_all_libraries, get_all_libranians
from django.template import loader
from .models import Library,Book
from .forms import BookForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import permission_required,login_required 


def display_all(request):
    insert_sample_data()
    if(insert_sample_data):
        print('Sample data inserted successfully.')
    else:
        print('Sample data insertion failed or already exists.')
    books = get_all_books()
    libraries = get_all_libraries()
    librarians = get_all_libranians()
    template = loader.get_template('index.html')
    context = {
        'books': books,
        'libraries': libraries,
        'librarians': librarians,
    }
    return HttpResponse(template.render(context, request))

def list_books(request):
    books = Book.objects.all().values()
    # template = loader.get_template('relationship_app/list_books.html')
    context = {
        'books': books,
    }   
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    """Display details for a specific library and its books."""
    model = Library
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optional: prefetch related books for performance
        context['books'] = self.object.books.select_related('author').all()
        template = loader.get_template('relationship_app/library_detail.html')
        return HttpResponse(template.render(context,self.request))

def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            login(request, user)  # Auto-login after registration
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# ----------------------------
# User Login View
# ----------------------------
def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('list_books')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


# ----------------------------
# User Logout View
# ----------------------------
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return render(request, 'relationship_app/logout.html')

# Use Django's built-in LoginView
class LoginView(LoginView):
    template_name = 'relationship_app/login.html'
    authentication_form = AuthenticationForm

# Use Django's built-in LogoutView
class LogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'



# Helper function to check if the user has a specific role
def check_role(user, role):
    return user.is_authenticated and user.userprofile.role == role

# Admin view
@login_required
@user_passes_test(lambda user: user.userprofile.role == 'Admin', login_url='home')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view
@login_required
@user_passes_test(lambda user: user.userprofile.role == 'Librarian', login_url='home')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view
@login_required
@user_passes_test(lambda user: user.userprofile.role == 'Member', login_url='home')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})