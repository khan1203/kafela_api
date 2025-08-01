
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__category', lookup_expr='iexact')
    is_available = django_filters.BooleanFilter()

    class Meta:
        model = Book
        fields = ['category', 'is_available']
