from django.shortcuts import render
from django.shortcuts import render
from django.db.models import Q
from .models import Book
from .forms import SearchForm
from .forms import ExampleForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# View Books (requires can_view)
@permission_required('bookself.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


# Create Book (requires can_create)
@permission_required('bookself.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('year')
        Book.objects.create(title=title, author=author, published_year=year)
        return redirect('book_list')

    return render(request, 'book_create.html')


# Edit Book (requires can_edit)
@permission_required('bookself.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_year = request.POST.get('year')
        book.save()
        return redirect('book_list')

    return render(request, 'book_edit.html', {'book': book})


# Delete Book (requires can_delete)
@permission_required('bookself.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')



def book_list(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'form': form
    })

def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # process data safely
            return render(request, 'bookshelf/form_success.html', {'form': form})
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})