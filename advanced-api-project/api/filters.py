import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Defines the filterable fields for the Book model.
    """
    # Allows exact matches on the publication year
    publication_year = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='exact'
    )
    
    # Allows filtering by Author name (using the foreign key relationship)
    author_name = django_filters.CharFilter(
        field_name='author__name', 
        lookup_expr='icontains', # case-insensitive containment
        label='Author Name (partial match)'
    )

    class Meta:
        model = Book
        fields = {
            # Standard filtering on publication_year (exact, lt, gt, etc.)
            'publication_year': ['exact', 'lt', 'gt', 'lte', 'gte'], 
            # Allows filtering by exact title match
            'title': ['exact'], 
        }