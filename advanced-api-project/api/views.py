# from rest_framework import generics, permissions, mixins
# from .models import Book
# from .serializers import BookSerializer

# # --- DRF Generic Views using Mixins for demonstration ---

# # 1. Book List and Create View (Equivalent to ListView + CreateView)
# class BookListCreateAPIView(mixins.ListModelMixin,
#                             mixins.CreateModelMixin,
#                             generics.GenericAPIView):
#     """
#     Handles listing all books (GET) and creating a new book (POST).
#     This combines the functionality of Django's ListView and CreateView for an API.
    
#     Permissions: Read access for all users, Write access for authenticated users.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     def get(self, request, *args, **kwargs):
#         # Calls ListModelMixin.list()
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         # Calls CreateModelMixin.create()
#         return self.create(request, *args, **kwargs)


# # 2. Book Detail, Update, and Destroy View (Equivalent to DetailView + UpdateView + DeleteView)
# class BookRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
#                                      mixins.UpdateModelMixin,
#                                      mixins.DestroyModelMixin,
#                                      generics.GenericAPIView):
#     """
#     Handles retrieving (GET), updating (PUT/PATCH), and deleting (DELETE) a single book.
#     This combines the functionality of Django's DetailView, UpdateView, and DeleteView for an API.

#     Permissions: Read access for all users, Write access for authenticated users.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     def get(self, request, *args, **kwargs):
#         # Calls RetrieveModelMixin.retrieve()
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         # Calls UpdateModelMixin.update()
#         return self.update(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         # Calls UpdateModelMixin.partial_update()
#         return self.partial_update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         # Calls DestroyModelMixin.destroy()
#         return self.destroy(request, *args, **kwargs)
from rest_framework import generics, mixins
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters 
from django_filters import rest_framework
from .filters import BookFilter
# --- Combined Views (Keep for List/Retrieve) ---

class BookListAPIView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    """Handles listing all books (GET) at /api/books/."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 2. Integrate the custom FilterSet
    filterSet_class = BookFilter
    
    # 3. Configure search fields (for SearchFilter)
    search_fields = ['title', 'author__name'] 
    
    # 4. Configure ordering fields (for OrderingFilter)
    ordering_fields = ['title', 'publication_year', 'author__name']
    # Optionally set default ordering
    ordering = ['title']
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BookRetrieveAPIView(mixins.RetrieveModelMixin,
                          generics.GenericAPIView):
    """Handles retrieving a single book (GET) at /api/books/<pk>/."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# --- Dedicated Views (New for Specific Paths) ---

class BookCreateAPIView(mixins.CreateModelMixin,
                        generics.GenericAPIView):
    """Handles creating a new book (POST) at /api/books/create/."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Requires authentication to create a book
    permission_classes = [IsAuthenticated] 
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BookUpdateAPIView(mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    """Handles updating a book (PUT/PATCH) at /api/books/<pk>/update/."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Requires authentication to update a book
    permission_classes = [IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class BookDeleteAPIView(mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    """Handles deleting a book (DELETE) at /api/books/<pk>/delete/."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Requires authentication to delete a book
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)