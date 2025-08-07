from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    FREEMIUM = 'FREEMIUM'
    PREMIUM = 'PREMIUM'
    USER_TYPES = [(FREEMIUM, 'Freemium'), (PREMIUM, 'Premium')]

    INSTITUTIONS = [
        ('BUBT', 'BUBT'), ('UIU', 'UIU'), ('NSU', 'NSU'), ('BRAC', 'BRAC'),
        ('AIUB', 'AIUB'), ('BUP', 'BUP'), ('College_Student', 'College Student'),
        ('Other', 'Other'),
    ]

    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    total_book_read = models.PositiveIntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=FREEMIUM)
    institution = models.CharField(max_length=20, choices=INSTITUTIONS, default='Other')
    student_id = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    total_pages = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class BookRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RETURNING', 'Want to Return'),
        ('RETURNED', 'Returned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user.username} -> {self.book.title} ({self.status})"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} on {self.book.title} [{self.rating}]"
