from django.contrib import admin
from .models import User, Book, BookRequest, Review, Category

# Register your models here.

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookRequest)
admin.site.register(Review)
admin.site.register(Category)
