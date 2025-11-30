
from rest_framework import status,test
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Author, Book
from datetime import date

# Define the view names based on api/urls.py
# Define the view names based on api/urls.py
LIST_URL = reverse('book-list')
CREATE_URL = reverse('book-create')

# Helper function to get detail URLs
def detail_url(pk):
    """Return book detail URL (GET)"""
    return reverse('book-detail', args=[pk])

def update_url(pk):
    """Return book update URL (PUT/PATCH)"""
    return reverse('book-update', args=[pk])

def delete_url(pk):
    """Return book delete URL (DELETE)"""
    return reverse('book-delete', args=[pk])


class BookAPITest(test.APITestCase):
    """Test suite for the Book API endpoints."""

    def setUp(self):
        """Set up environment: client, users, author, and initial books."""
        self.client = self.client # DRF APIClient

        # Authentication credentials
        self.username = 'authuser'
        self.password = 'testpassword'
        
        # Create a regular user
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        
        # Create an Author instance required by the Book model
        self.author1 = Author.objects.create(name='Jane Austen')
        self.author2 = Author.objects.create(name='Stephen King')

        # Create initial Book instances
        self.book1 = Book.objects.create(
            title='Pride and Prejudice', publication_year=1813, author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Shining', publication_year=1977, author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Sense and Sensibility', publication_year=1811, author=self.author1
        )
        
        # Test data for POST request
        self.payload = {
            'title': 'New Book Title',
            'publication_year': date.today().year,
            'author': self.author2.id, # Must include a valid Author ID
        }

    # --- PERMISSIONS TESTING ---

    def test_create_book_requires_authentication(self):
        """Test POST to /create/ fails without authentication."""
        response = self.client.post(CREATE_URL, self.payload, format='json')
        # Expect 403 Forbidden because permission_classes = [IsAuthenticated]
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_requires_authentication(self):
        """Test PUT to /update/ fails without authentication."""
        url = update_url(self.book1.id)
        response = self.client.put(url, {'title': 'New Title'}, format='json')
        # Expect 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_requires_authentication(self):
        """Test DELETE to /delete/ fails without authentication."""
        url = delete_url(self.book1.id)
        response = self.client.delete(url)
        # Expect 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_list_and_retrieve_allow_unauthenticated(self):
        """Test GET requests are allowed for unauthenticated users."""
        # Test List View
        list_response = self.client.get(LIST_URL)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        # Test Detail View
        detail_response = self.client.get(detail_url(self.book1.id))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)


    # --- CRUD FUNCTIONALITY TESTING (Authenticated) ---

    def test_create_book_success(self):
        """Test creating a book with valid data and authentication using login."""
        # Use self.client.login() to establish a session for the authenticated user
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(CREATE_URL, self.payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4) # 3 initial + 1 new
        self.assertEqual(response.data['title'], self.payload['title'])
        self.assertEqual(response.data['author'], self.payload['author'])
        # Log out to ensure subsequent unauthenticated tests are not affected (optional, but good practice)
        self.client.logout()

    def test_create_book_invalid_year_fails(self):
        """Test creating a book with a future publication year fails validation."""
        self.client.login(username=self.username, password=self.password)
        invalid_payload = self.payload.copy()
        invalid_payload['publication_year'] = date.today().year + 1
        
        response = self.client.post(CREATE_URL, invalid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the custom validation error is present
        self.assertIn('publication_year', response.data)
        self.assertIn('Publication year cannot be in the future', str(response.data['publication_year']))
        self.client.logout()

    def test_retrieve_book_success(self):
        """Test retrieving a book by ID."""
        # GET requests are allowed by unauthenticated users, no login needed
        response = self.client.get(detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_update_book_success(self):
        """Test updating a book using PUT (full update) with login."""
        self.client.login(username=self.username, password=self.password)
        url = update_url(self.book1.id)
        new_year = 2005
        # Note: PUT requires all required fields, but the serializer omits 'author' as read_only_fields are set.
        updated_payload = {
            'title': 'New P&P Title',
            'publication_year': new_year
        }
        
        response = self.client.put(url, updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'New P&P Title')
        self.assertEqual(self.book1.publication_year, new_year)
        self.client.logout()

    def test_partial_update_book_success(self):
        """Test partially updating a book using PATCH with login."""
        self.client.login(username=self.username, password=self.password)
        url = update_url(self.book1.id)
        
        response = self.client.patch(url, {'title': 'Only Title Change'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Only Title Change')
        self.assertEqual(self.book1.publication_year, 1813) 
        self.client.logout()

    def test_delete_book_success(self):
        """Test deleting a book with login."""
        self.client.login(username=self.username, password=self.password)
        book_id = self.book2.id
        url = delete_url(book_id)
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book_id).exists())
        self.assertEqual(Book.objects.count(), 2)
        self.client.logout()

    # --- QUERY FUNCTIONALITY TESTING ---

    def test_list_filter_by_year(self):
        """Test filtering by publication_year (exact)."""
        response = self.client.get(LIST_URL, {'publication_year': 1813})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_filter_by_author_name(self):
        """Test filtering by author_name (icontains)."""
        response = self.client.get(LIST_URL, {'author_name': 'jane'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_search_by_title_and_author(self):
        """Test searching across title and author__name fields."""
        response = self.client.get(LIST_URL, {'search': 'king'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_ordering_by_publication_year(self):
        """Test ordering by publication_year (descending)."""
        response = self.client.get(LIST_URL, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The Shining (1977) should be first
        self.assertEqual(response.data[0]['title'], self.book2.title)