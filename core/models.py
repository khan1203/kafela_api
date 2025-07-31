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
